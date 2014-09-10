#!/bin/bash
mv homes.csv 2homes.csv
python rssFeedParser.py
#sleep 2
vimdiff homes.csv 2homes.csv
