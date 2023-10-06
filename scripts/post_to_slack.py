import requests
import os
import datetime

today = datetime.date.today().strftime('%m-%d-%Y')

stdout_file_path=f"/Users/ekim/workspace/personal/dd-bot/dev/build/logs/stdout/{today}_out.log"
stderr_file_path=f"/Users/ekim/workspace/personal/dd-bot/dev/build/logs/stderr/{today}_err.log"

# TODO
# File paths stage
# stdout_file_path = f'C:\\Users\\ekima\\workspace\\DTN BOT\\stdout\\{today}_out.log'
# stderr_file_path = f'C:\\Users\\ekima\\workspace\\DTN BOT\\stderr\\{today}_err.log'

# File paths prod
# stdout_file_path = f'C:\\Users\\bots\\workspace\\DTN BOT\\stdout\\{today}_out.log'
# stderr_file_path = f'C:\\Users\\bots\\workspace\\DTN BOT\\stderr\\{today}_err.log'

# OAuth token with `files:write`
slack_token = os.getenv('SLACK_OAUTH_TOKEN')

def post_to_slack(file_path, slack_token):
    """Upload a file to a Slack channel."""

    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"The file {file_path} does not exist.")
        return

    # Extract file name from the path
    file_name = os.path.basename(file_path)
    title = f"*{file_name}*"

    # Slack's files.upload endpoint
    upload_url = "https://slack.com/api/files.upload"

    headers = {
        'Authorization': f"Bearer {slack_token}",
    }

    # Use the file's content to create a payload for the POST request
    with open(file_path, "rb") as file:
        files = {
            'file': (file_name, file),
        }
        data = {
            'channels': '#dd_bot_orders',
            'title': title,
            'filename': file_name,
        }

        response = requests.post(upload_url, headers=headers, data=data, files=files)

    # Check response
    json_response = response.json()
    if not json_response.get("ok"):
        raise ValueError(f'Error uploading file to Slack: {json_response.get("error")}')


# Upload stdout and stderr to Slack #dtn_bot channel
def main():
    # Always post stderr first
    try:
        post_to_slack(stderr_file_path, slack_token)
    except Exception as e:
        print(f"Error posting stderr file: {e}")

    # Then post stdout
    try:
        post_to_slack(stdout_file_path, slack_token)
    except Exception as e:
        print(f"Error posting stdout file: {e}")


if __name__ == "__main__":
    main()
