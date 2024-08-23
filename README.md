# rasa-hello


```
rasa train

# one terminal
rasa run --enable-api --cors "*" --debug

# second terminal
rasa run actions --debug

# test terminal or double click chatbot.html
curl -X POST http://localhost:5005/webhooks/rest/webhook -d '{"sender": "default", "message": "Hi"}'
```