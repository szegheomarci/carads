#!/bin/bash

cd test

docker run  \
       -v ./config:/app/config \
       -v ./input:/app/input \
       -v ./processed:/app/processed \
       $1
