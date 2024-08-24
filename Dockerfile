FROM rasa/rasa:3.6.20-full

USER root

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

USER rasa

ENV RUN_IN_DOCKER=True