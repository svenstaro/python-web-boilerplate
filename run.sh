#!/bin/bash

hypercorn -b 0.0.0.0:5000 -w 1 --error-logfile - --access-logfile - app:app 
