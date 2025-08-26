#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ps -eaf | grep -i "paperlessngx_postprocessor.py" | grep -v grep
# if not found - equals to 1, start it
if [ $? -eq 1 ]
then
echo "eq 0 - paperlessngx_postprocessor not running"
#printenv
#$DIR/venv/bin/python3 $DIR/paperlessngx_postprocessor.py --verbose DEBUG process --tag Refresh
cd $DIR/venv/bin/
python3 "$DIR/paperlessngx_postprocessor.py" --verbose DEBUG process --tag "${PNGX_POSTPROCESSOR_POSTPROCESSING_INPUT_TAG}" > /var/log/pngxscript.log 2>&1
else
echo "eq 0 - paperlessngx_postprocessor running - do nothing"
fi