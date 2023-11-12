#!/bin/bash

cd test

docker run szegheomarci/dbloader:$1-$2 \
       -v config:/app/src/config \
       -v input:/app/src/input \
       -v processed:/app/src/processed
