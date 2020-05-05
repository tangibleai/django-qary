#!/usr/bin/env bash
#test_aliveness.sh

if [ $(curl -q http://totalgood.org/midata/models/qa/ | grep -F 'albert-large-v2-0.2.0.zip' | wc | cut -c7-8) == '1' ] ; then
    echo PASSED
else
    echo "FAILED: nginx is failing to serve http://totalgood.org/midata/models/qa/albert-large-v2-0.2.0.zip"
fi

if [ $(curl -q http://totalgood.org/connect/ wc | cut -c7-8) == '1' ] ; then
    echo "FAILED: elastic search and django are failing to serve http://totalgood.org/connect/"
else
    echo PASSED
fi

