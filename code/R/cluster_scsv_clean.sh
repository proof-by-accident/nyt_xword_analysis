#!/bin/bash

sed 's/"//g' cluster_examps.scsv | sed 's/,//g' | sed 's/;/,/g' | sed 's/\\//g' | sed 's/cluster./Cluster /g' > cluster_examps.csv
