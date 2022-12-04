#!/bin/bash

ads_table="ads"
#Define multi-character delimiter
delimiter="####"

run_query () {
  docker exec -i db-mysql mysql -u root -pmy-secret-pw proba1 < $1
}

# iterate through the input files
for inputfile in $(ls ./input); do
  # create input table
  ###############################
  table_name="t${inputfile}"
  add_date="$(echo ${table_name} | sed -E "s|.*([0-9][0-9][0-9][0-9])([0-9][0-9])([0-9][0-9])_.*|\1-\2-\3|")"
  echo "creating table ${table_name}"
  query="CREATE TABLE ${table_name} ( "
  query+='`asID` varchar(255), '
  query+='`Title` varchar(255), ' 
  query+='`Subtitle` varchar(255), '
  query+='`Price` varchar(255), '
  query+='`Mileage` varchar(255), '
  query+='`ManufDate` DATE, '
  query+='`Engine` varchar(255), '
  query+='`Seller` varchar(255), '
  query+='`Country` varchar(255), '
  query+='`Address` varchar(255), '
  query+='`Link` varchar(255), '
  query+='`Color` varchar(255), '
  query+='`PriceEuro` INT, '
  query+='`MileageKm` INT, '
  query+='`Start_Date` DATE);'
  echo ${query} > query.sql
  run_query query.sql

  # create input records
  ###############################
  query="INSERT INTO \`${table_name}\` ( "
  query+='`asID`, `Title`, `Subtitle`, `Price`, `Mileage`, `ManufDate`, `Engine`, `Seller`, `Country`, `Address`, `Link`, `Color`,  `PriceEuro`, `MileageKm`, `Start_Date`) VALUES '
  nextrecordcomma=""
  
  while read line; do
    # the last line is empty, skip that
    [[ -z ${line} ]] && break

    input=${line}${delimiter}
    values=()
    while [[ ${input} ]]; do
      values+=( "${input%%"${delimiter}"*}" )
      input="${input#*"${delimiter}"}"
    done

    # ManufDate to date
    values[5]=$(echo "${values[5]}" | sed -E "s|([0-9][0-9])/([0-9][0-9][0-9][0-9])|\2-\1-15|")
    # if country is empty, copy from address
    if [ -z ${values[8]} ] ; then
      #                                     need -E for extended regex
      values[8]=$(echo "${values[9]}" | sed -E "s|.*?([A-Z][A-Z]).*?|\1|") || values[8]="unknown"
    fi
    # get color
    color="${values[10]%%"-${values[0]}"*}"
    color="${color##*"-"}"
    if [[ ${color} == "gasoline" ]] ; then
      color="unknown"
    fi
    # switch to int
    price=$(echo "${values[3]}" | sed -E "s|[^0-9]||g")
    kms=$(echo "${values[4]}" | sed -E "s|[^0-9]||g")
    #price="${values[3]//[^[0-9]]/}"
    #kms="${values[4]//[^[0-9]]/}"

    # write record
    query+="$(echo "${nextrecordcomma}( " )"
    for ((i = 0; i < ${#values[@]}; i++)) ; do
      # if variable is empty, set it to null
      [[ -z ${values[$i]} ]] && values[$i]="Null"
      #printf -v escaped "%q" "${values[$i]}"
      escaped="$(echo "${values[$i]}" | sed -E "s|([\"'\\])|\\\\\1|g")" #| sed -e "s|\*|-o-|g"
      query+="$(echo "'${escaped}'," )"
    done
    
    #                                   the euro symbol survived the sed replace, must be removed
    query+="$(echo " '${color}', '${price//[^[:ascii:]]/}', '${kms}', '${add_date}' )" )"
    
    nextrecordcomma=", "

  done < ./input/${inputfile}
  
  echo "Adding data to input table."
  echo "${query}" > query.sql
  run_query query.sql
exit 0
  
  # Update the ads table
  ###############################
  # all ads present in the input table must have NULL End_Date in the ads table
  query="UPDATE \`${ads_table}\` SET "
  query+='`End_Date`=NULL WHERE `End_Date` IS NOT NULL AND `asID` IN (SELECT `asID` FROM '
  query+="\`${table_name}\`);"
  echo "Erasing end date in ads table for reappearing ads."
  echo ${query} > query.sql
  run_query query.sql

  # remove ads from input already in ads table
  query="DELETE FROM \`${table_name}\` "
  query+='WHERE `asID` IN (SELECT `asID` FROM '
  query+="\`${ads_table}\`);"
  echo "Removing ads from input table already in ads table."
  echo ${query} > query.sql
  run_query query.sql

  # insert input table records in case of new ads
  query="INSERT INTO \`${ads_table}\` "
  query+='(`asID`, `Title`, `Subtitle`, `Price`, `Mileage`, `ManufDate`, `Engine`, `Seller`, `Country`, `Address`, `Link`, `Color`, `PriceEuro`, `MileageKm`, `Start_Date`) '
  query+='SELECT `asID`, `Title`, `Subtitle`, `Price`, `Mileage`, `ManufDate`, `Engine`, `Seller`, `Country`, `Address`, `Link`, `Color`, `PriceEuro`, `MileageKm`, `Start_Date` '
  query+="FROM \`${table_name}\`;"
  echo "Adding new ads to ads table."
  echo ${query} > query.sql
  run_query query.sql

  # delete input table
  echo "DROP TABLE  \`${table_name}\`;" > query.sql
  echo "Removing temporary input table."
  run_query query.sql

done

echo "all input files complete"
