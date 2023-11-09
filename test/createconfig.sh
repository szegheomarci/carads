#!/bin/bash

pwd
ls -l
cp test/config.yaml src/config/config.yaml
sed -i -e "s|@hostaddress@|$1|" -e "s|@port@|$2|" -e "s|@password@|$3|" -e "s|@dbname@|$4|" src/config/config.yaml

echo "Prepared config file:"
cat src/config/config.yaml
