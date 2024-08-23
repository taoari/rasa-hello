# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os

LOCALHOST = 'host.docker.internal' if os.environ.get('RUN_IN_DOCKER') else 'localhost'

from gradio_client import Client

CACHE = dict(clients={})

def _gradio_chat(message, sender_id=None):
    global CACHE
    if sender_id not in CACHE['clients']:
        CACHE['clients']['sender_id'] = Client(f"http://{LOCALHOST}:7860/")
    client = CACHE['clients']['sender_id']
    
    result = client.predict(
            message,	# str  in 'Message' Textbox component
            None,	# str (filepath on your computer (or URL) of image) in 'Input' Image component
            "",	# str  in 'System prompt' Textbox component
            "auto",	# str  in 'Chat engine' Radio component
            "auto",	# str  in 'Bot response format' Radio component
            False,	# bool  in 'Speech Synthesis' Checkbox component
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
        # dispatcher.utter_message(text=f"I received {user_message} from {sender_id}")
        dispatcher.utter_message(text=_gradio_chat(user_message))

        return []
