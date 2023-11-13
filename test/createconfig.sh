#!/bin/bash

mkdir -p test/config
cp test/config.yaml test/config/config.yaml

#sed -i -e "s|@hostaddress@|$1|" -e "s|@port@|$2|" -e "s|@user@|$3|" -e "s|@password@|$3|" -e "s|@dbname@|$4|" test/config/config.yaml
sed -i -e "s|@hostaddress@|${HOST}|" -e "s|@port@|${PORT}|" -e "s|@user@|${USERNAME}|" -e "s|@password@|${PASSWORD}|" -e "s|@dbname@|${DBNAME}|" test/config/config.yaml
