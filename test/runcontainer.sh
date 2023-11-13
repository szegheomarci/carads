#!/bin/bash

cd test
pwd
ls -l
echo "input:"
ls -l input
echo "processed:"
ls -l processed

docker run  \
       -v ./config:/app/config \
       -v ./input:/app/input \
       -v ./processed:/app/processed \
       szegheomarci/dbloader:$1-$2
