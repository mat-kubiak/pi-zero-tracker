#!/bin/sh

_script_dir="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
log_mes="\n\n##### [Starting Session at $(date '+%Y-%m-%d %H:%M:%S')]\n"

cd $_script_dir
echo -e "$log_mes" >> log
source "./testenv/bin/activate" &>>log
python3 "./main.py" &>> log
