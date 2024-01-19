CREATE TABLE ads (
    id INT NOT NULL AUTO_INCREMENT,
    asID varchar(255),
    Title varchar(255),
    Subtitle varchar(255),
    Price varchar(25),
    PriceEuro INT,
    Mileage varchar(255),
    MileageKm INT,
    ManufDate DATE,
    Engine varchar(255),
    Seller varchar(255),
    Country varchar(255),
    Address varchar(255),
    Color varchar(255),
    Link varchar(255),
    Start_Date DATE,
    End_Date DATE,
    PRIMARY KEY (`id`)
);


CREATE TABLE years (
    id INT NOT NULL AUTO_INCREMENT,
    yr INT,
    PRIMARY KEY (`id`)
);
INSERT INTO `years` (`yr`) VALUES
(2018),(2019),(2020),(2021),(2022),(2023),(2024),(2025),(2026),(2027),(2028);

CREATE TABLE weeks (
    id INT NOT NULL AUTO_INCREMENT,
    ord INT,
    start varchar(10),
    end varchar(10),
    PRIMARY KEY (`id`)
);
INSERT INTO `weeks` (`ord`, `start`, `end`) VALUES
(1, '01-01', '01-07'),(2, '01-08', '01-14'),(3, '01-15', '01-21'),(4, '01-22', '01-28'),(5, '01-29', '02-04'),(6, '02-05', '02-11'),(7, '02-12', '02-18'),(8, '02-19', '02-25'),(9, '02-26', '03-04'),(10, '03-05', '03-11'),(11, '03-12', '03-18'),(12, '03-19', '03-25'),(13, '03-26', '04-01'),(14, '04-02', '04-08'),(15, '04-09', '04-15'),(16, '04-16', '04-22'),(17, '04-23', '04-29'),(18, '04-30', '05-06'),(19, '05-07', '05-13'),(20, '05-14', '05-20'),(21, '05-21', '05-27'),(22, '05-28', '06-03'),(23, '06-04', '06-10'),(24, '06-11', '06-17'),(25, '06-18', '06-24'),(26, '06-25', '07-01'),(27, '07-02', '07-08'),(28, '07-09', '07-15'),(29, '07-16', '07-22'),(30, '07-23', '07-29'),(31, '07-30', '08-05'),(32, '08-06', '08-12'),(33, '08-13', '08-19'),(34, '08-20', '08-26'),(35, '08-27', '09-02'),(36, '09-03', '09-09'),(37, '09-10', '09-16'),(38, '09-17', '09-23'),(39, '09-24', '09-30'),(40, '10-01', '10-07'),(41, '10-08', '10-14'),(42, '10-15', '10-21'),(43, '10-22', '10-28'),(44, '10-29', '11-04'),(45, '11-05', '11-11'),(46, '11-12', '11-18'),(47, '11-19', '11-25'),(48, '11-26', '12-02'),(49, '12-03', '12-09'),(50, '12-10', '12-16'),(51, '12-17', '12-23'),(52, '12-24', '12-31');

CREATE VIEW vWeeks AS SELECT `ord` AS weeknum, `yr` as year, STR_TO_DATE(CONCAT(`yr`,'-',`start`),"%Y-%c-%d") AS weekstart, STR_TO_DATE(CONCAT(`yr`,'-',`end`),"%Y-%c-%d") AS weekend, CONCAT('ads',`yr`,'w',`ord`) AS tablename
FROM `years`, `weeks`
WHERE STR_TO_DATE(CONCAT(`yr`,'-',`start`),"%Y-%c-%d") BETWEEN '2018-09-16' AND CURRENT_DATE
--                                                     start of data collection is 2018-09-17
ORDER BY weekstart;

CREATE VIEW vColors AS SELECT DISTINCT `Color` FROM `ads` ORDER BY `Color`;
CREATE VIEW vCountries AS SELECT DISTINCT `Country` FROM `ads` ORDER BY `Country`;

CREATE VIEW vAdsByWeek AS SELECT
CONCAT("W", `vWeeks`.`weeknum`, "/", `vWeeks`.`year`) AS weeknumber, `vWeeks`.`year`, `vWeeks`.`weeknum`,`vWeeks`.`weekstart`,
`ads`.`PriceEuro`, `ads`.`MileageKm`, `ads`.`ManufDate`, `ads`.`Engine`, `ads`.`Color`, `ads`.`Seller`, `ads`.`Country`,
`ads`.`Address`, DATEDIFF(IFNULL(`ads`.`End_Date`,CURRENT_DATE()), `ads`.`Start_Date`) AS ActiveDays
FROM `vWeeks`, `ads`
WHERE `ads`.Start_Date <= `vWeeks`.`weekend` AND (`ads`.End_Date >= `vWeeks`.`weekstart` OR `ads`.`End_Date` IS Null)
ORDER BY `vWeeks`.`weekstart` ASC;
