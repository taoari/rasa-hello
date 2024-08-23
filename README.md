# rasa-hello


```
rasa train

# one terminal
rasa run --enable-api --cors "*" --debug

# second terminal
rasa run actions --debug

# test terminal or double click `webui/index.html`
curl -X POST http://localhost:5005/webhooks/rest/webhook -d '{"sender": "default", "message": "Hi"}'
```

## Docker Demo Setup

* Train (one time)

```
docker run -v .:/app rasa/rasa:3.6.20-full train
```

* Setup Demo

```bash
docker compose up -d
docker compose down
```

* Demo is setup at http://localhost:5000/

## Learning

### Rasa Fallback

https://rasa.com/docs/rasa/fallback-handoff/

### Custom Action

https://github.com/RasaHQ/conversational-ai-course-3.x

