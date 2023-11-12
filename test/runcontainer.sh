#!/bin/bash

docker run szegheomarci/dbloader:$1-$2 \
       -v test/config:/app/src/config \
       -v test/input:/app/src/input \
       -v test/processed:/app/src/processed
