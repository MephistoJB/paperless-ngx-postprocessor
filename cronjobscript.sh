#!/bin/bash
ps -eaf | grep -i "paperlessngx_postprocessor.py" | grep -v grep
# if not found - equals to 1, start it
if [ $? -eq 1 ]
then
#echo "eq 0 - paperlessngx_postprocessor not running"
printenv
#/usr/src/paperless/paperless-ngx_postprocessor/venv/bin/python3 /usr/src/paperless/paperless-ngx_postprocessor/paperlessngx_postprocessor.py --verbose DEBUG process --tag Refresh
/usr/src/paperless/paperless-ngx_postprocessor/venv/bin/python3 /usr/src/paperless/paperless-ngx_postprocessor/paperlessngx_postprocessor.py --verbose --tag Refresh
else
echo "eq 0 - paperlessngx_postprocessor running - do nothing"
fi