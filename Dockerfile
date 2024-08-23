FROM rasa/rasa:3.6.20-full

ENV RUN_IN_DOCKER=True

USER root

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

USER rasa