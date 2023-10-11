#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate bots
export SLACK_OAUTH_TOKEN="xoxb-4099486963537-6000372605090-4MtiYma3T9ewvSzDJmqavbQc"
today=$(date +"%m-%d-%Y")

# Get operating system name
os_name=$(uname -a | awk '{print $1}')
# if MINGW64 == WSL within git bash ; if Darwin = mac ==> dev env
echo "Currently using operating system: $os_name"

# Parse config using yq and set vars; see https://github.com/mikefarah/yq for more info
if [[ $os_name == 'Darwin' ]]; then  # dev
  echo "Setting env vars for DEV environment"

  workspace_type=$(yq e '.dev.workspace_type' $HOME/workspace/personal/dd-bot/src/config.yaml)

  export PYTHONPATH="$HOME/workspace/${workspace_type}/dd-bot/src"
  echo "PYTHONPATH has been set to: $PYTHONPATH"

  config_yaml_path="$PYTHONPATH/config.yaml"

  username=$(yq e '.dev.username' $config_yaml_path)
  echo "Username has been set to: $username"

  home_dir=$(yq e '.dev.home_dir' $config_yaml_path)

  # Replace {username} with actual username
  home_dir={$home_dir//'{username}'/$username}
  echo "Home directory has been set to: $home_dir"


  json_build_tail_dir=$(yq e '.dev.json_build_tail_dir' $config_yaml_path)
  stdout_dir="$home_dir$json_build_tail_dir/logs/stdout"
  stderr_dir="$home_dir$json_build_tail_dir/logs/stderr"

  echo "Redirecting standard output to ${stdout_dir}/${today}_out.log"
  echo "Redirecting standard error to ${stderr_dir}/${today}_err.log"

  echo "Posting stderr and stdout to Slack channel"
  python "$home_dir$workspace_type/dd-bot/scripts/post_to_slack.py"



else  # stage env
  workspace_type=$(yq e '.stage.workspace_type' $HOME/workspace/txb/dd-bot/src/config.yaml)

  export PYTHONPATH="$HOME/workspace/${workspace_type}/dd-bot/src"
  echo "PYTHONPATH has been set to: $PYTHONPATH"

  config_yaml_path="$PYTHONPATH/config.yaml"

  username=$(yq e '.stage.username' $config_yaml_path)
  echo "Username has been set to: $username"

  home_dir=$(yq e '.dev.home_dir' $config_yaml_path)

  json_build_tail_dir=$(yq e '.stage.json_build_tail_dir' $config_yaml_path)
  stdout_dir="$home_dir/$json_build_tail_dir/logs/stdout"
  stderr_dir="$home_dir/$json_build_tail_dir/logs/stderr"

  echo "Redirecting standard output to ${stdout_dir}/${today}_out.log"
  echo "Redirecting standard error to ${stderr_dir}/${today}_err.log"

  python "$home_dir/$workspace_type/dd-bot/scripts/post_to_slack.py"




fi
#
## todo: prod env setting
#  # Print the current working directory
#  echo "The current working directory is: $(pwd)"
#
#  # Change directories to repo; @dev: only req'd for prod
#  cd /c/Users/ekima/workspace/txb/dd-bot
#
#  # Confirm changed directories
#  echo "The new current working directory is: $(pwd)"
#
## Run entrypoint, redirect stdout (print stmts only) and stderr (logging module logs only), sanitize via `sed` to remove ANSI escapes (from coloring logs)
#python -m src.app.__main__ > "${stdout_dir}/${today}_out.log" 2> >(sed 's/\x1b\[[0-9;]*m//g' > "${stderr_dir}/${today}_err.log")
#
#
#echo "Redirection complete. Check ${stdout_dir}/${today}_out.log and ${stderr_dir}/${today}_err.log for logs."
#
#
## prod # todo
#python /c/Users/ekima/workspace/txb/dd-bot/scripts/post_to_slack.py
