# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from dotenv import load_dotenv

load_dotenv()

import os
import logging
import re

logger = logging.getLogger(__name__)

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import uuid
from gradio_client import Client
logging.getLogger("httpx").setLevel(logging.WARNING) # Disable printing unwanted messages

client = Client(os.environ.get('GRADIO_SERVER'))

def _gradio_chat(message, session_hash=None):
    client.session_hash = session_hash if session_hash is not None else str(uuid.uuid4())
    
    result = client.predict(
            message,	# str  in 'Message' Textbox component
            api_name="/chat"
    )
    return result

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        sender_id = tracker.current_state()['sender_id']
        user_message = tracker.latest_message.get('text')
        channel = tracker.get_latest_input_channel()

        logger.info(f'Received message: {dict(user_message=user_message, sender_id=sender_id, channel=channel)}"')
        text = re.sub(r'\n+', '\n', _gradio_chat(user_message, sender_id))
    
        if channel == 'slack':
            # NOTE: slack markdown format is different from classic markdown format
            # refer to https://app.slack.com/block-kit-builder for slack Block Kit Builder
            dispatcher.utter_message(custom={'text': text, 'mrkdwn': True})
        else:
            dispatcher.utter_message(text=text)

        return []
    
if __name__ == '__main__':
    # client = Client(os.environ.get('GRADIO_SERVER'))
    print(_gradio_chat('Hello, my name is Alice.', session_hash='123'))
    print(_gradio_chat('Hello, my name is Bob.', session_hash='456'))
    print(_gradio_chat('What is my name?', session_hash='123'))
    print(_gradio_chat('What is my name?', session_hash='456'))

