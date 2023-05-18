import os
import re

from slack_bolt import App  
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
from slack_sdk.web import WebClient

from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

from spreadsheet import Spreadsheet

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],    
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

def find_url(string):
 
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]

@app.message("")
def on_message_sent(event, client: WebClient):
    text = event.get("text")
    urls = '\n'.join(find_url(event.get("text")))
    print(urls)
    userid = event.get("user")
    response = client.users_info(user=userid)
    username = response["user"]["name"]
    current_time = str(datetime.now().strftime("%Y-%m-%d"))
    info_dict = {
        "Time Sent": [current_time],
        "Sender": [username],
        "Content": [text],
        "Urls": [urls],

    }
    Spreadsheet(data=info_dict).run()
    


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()