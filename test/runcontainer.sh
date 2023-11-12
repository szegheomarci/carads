#!/bin/bash

cd test
pwd
ls -l

docker run  \
       -v ./config:/app/config \
       -v ./input:/app/input \
       -v ./processed:/app/processed \
       szegheomarci/dbloader:$1-$2
