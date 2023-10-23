#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate bots
export PYTHONPATH="$HOME/workspace/personal/dd-bot/src/"
export SLACK_OAUTH_TOKEN="xoxb-4099486963537-6000372605090-4MtiYma3T9ewvSzDJmqavbQc"

echo "PYTHONPATH has been set to: $PYTHONPATH"

today=$(date +"%m-%d-%Y")

# Define the output directories
stdout_dir="/Users/ekim/workspace/personal/dd-bot/dev/build/logs/stdout"
stderr_dir="/Users/ekim/workspace/personal/dd-bot/dev/build/logs/stderr"

# --------------------------------------  prod  ----------------------------------------
#stdout_dir="C:/Users/ekima/workspace/doordash/logs/stdout"
#stderr_dir="C:/Users/ekima/workspace/doordash/logs/stderr"

## Print the current working directory
#echo "The current working directory is: $(pwd)"
#
## Change directories to repo
## shellcheck disable=SC2164
#cd /c/Users/ekima/workspace/txb/dd-bot
#
## Confirm changed directories
#echo "The new current working directory is: $(pwd)"
# --------------------------------------  prod  ----------------------------------------





echo "Redirecting standard output to ${stdout_dir}/${today}_out.log"
echo "Redirecting standard error to ${stderr_dir}/${today}_err.log"

# Print the current working directory
echo "The current working directory is: $(pwd)"

# Run entrypoint, redirect stdout (print stmts only) and stderr (logging module logs only), sanitize via `sed` to remove ANSI escapes (from coloring logs)
python -m src.app.__main__  > "${stdout_dir}/${today}_out.log" 2> >(sed 's/\x1b\[[0-9;]*m//g' > "${stderr_dir}/${today}_err.log")

echo "Redirection complete. Check ${stdout_dir}/${today}_out.log and ${stderr_dir}/${today}_err.log for logs."

echo "Posting stderr and stdout to Slack channel"
python /Users/ekim/workspace/personal/dd-bot/scripts/post_to_slack.py
