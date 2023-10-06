#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate bots
export PYTHONPATH="$HOME/workspace/personal/dd-bot/src/"
export SLACK_OAUTH_TOKEN="xoxb-4099486963537-5704022177687-ZVzgnbQHqtX2FzO8svV4ziCI"

echo "PYTHONPATH has been set to: $PYTHONPATH"

today=$(date +"%m-%d-%Y")

# Define the output directories
stdout_dir="/Users/ekim/workspace/personal/dd-bot/dev/build/logs/stdout"
stderr_dir="/Users/ekim/workspace/personal/dd-bot/dev/build/logs/stderr"

# prod stdout/stderr
#stdout_dir="C:/Users/bots/workspace/doordash/stdout"
#stderr_dir="C:/Users/bots/workspace/doordash/stderr"

echo "Redirecting standard output to ${stdout_dir}/${today}_out.log"
echo "Redirecting standard error to ${stderr_dir}/${today}_err.log"

# Print the current working directory
echo "The current working directory is: $(pwd)"

# Run the entrypoint python script and redirect stdout and stderr
python -m src.app.__main__ > "${stdout_dir}/${today}_out.log" 2> "${stderr_dir}/${today}_err.log"

echo "Redirection complete. Check ${stdout_dir}/${today}_out.log and ${stderr_dir}/${today}_err.log for logs."

echo "Posting stderr and stdout to Slack channel"
python /Users/ekim/workspace/personal/dd-bot/scripts/post_to_slack.py
