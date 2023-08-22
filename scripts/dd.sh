#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate bots
export DD_MERCHANT_LOGIN_URL="https://identity.doordash.com/auth?client_id=1643580605860775164&redirect_uri=https%3A%2F%2Fmerchant-portal.doordash.com%2Fauth_callback&scope=*&prompt=none&response_type=code&layout=merchant_web_v2&state=8b164938-6941-4894-99b8-24c290027440&allowRedirect=true&failureRedirect=%2Fmerchant%2Flogin"
export DEV_LOGIN_PASSWORD="3%rV@c7ixWgYVn"
export DEV_LOGIN_EMAIL="ekim@txbstores.com"
export PYTHONPATH="$HOME/workspace/dd-bot/"
export SLACK_OAUTH_TOKEN="xoxb-4099486963537-5704022177687-ZVzgnbQHqtX2FzO8svV4ziCI"
echo "PYTHONPATH has been set to: $PYTHONPATH"
echo "DEV_LOGIN_EMAIL has been set to: $DEV_LOGIN_EMAIL"
echo "DEV_LOGIN_PASSWORD has been set to: $DEV_LOGIN_PASSWORD"
echo "DD_MERCHANT_LOGIN_URL has been set to: $DD_MERCHANT_LOGIN_URL"

today=$(date +"%m-%d-%Y")

# Define the output directories
stdout_dir="C:/Users/bots/workspace/doordash/stdout"
stderr_dir="C:/Users/bots/workspace/doordash/stderr"

echo "Redirecting standard output to ${stdout_dir}/${today}_out.log"
echo "Redirecting standard error to ${stderr_dir}/${today}_err.log"

# Print the current working directory
echo "The current working directory is: $(pwd)"

# Run the entrypoint python script and redirect stdout and stderr
#python -m src.test.main > "${stdout_dir}/${today}_out.log" 2> "${stderr_dir}/${today}_err.log"

echo "Redirection complete. Check ${stdout_dir}/${today}_out.log and ${stderr_dir}/${today}_err.log for logs."

echo "Posting stderr and stdout to Slack channel"
#python /c/Users/ekima/workspace/dd-bot/scripts/post_to_slack.py
