#!/bin/bash

cd test

docker run  \
       -v config:/app/src/config \
       -v input:/app/src/input \
       -v processed:/app/src/processed \
       szegheomarci/dbloader:$1-$2
