# django-bot-server-tutorial

Accompanying repository for a seminar on creating a django based bot server and also getting started with django-channels

# First part

This part of the seminar involves setting up a bot server to connect to Telegram API via webhook and to respond to some messages with yo mama jokes.

## Before getting started

Make sure oyu have the following

- pip
- virtualenv
- git
- Telegram messenger, preferebly on your work machine

## What to do

To get this running, you need the following. First install dependencies

`pip install -r requirements.txt`

Then get your database started with all the migrations

`python manage.py migrate`

And start the server with 

`python manage.py runserver`

Download ngrok (https://ngrok.com/) and start it with 

`ngrok http 8000`

Talk to the botfather on telegram and give the command /newbot to create a bot and get a token

Update the token in views.py.

Do a get request to set the webhook for your bot. 
Run the following command in your terminal (assuming a unix terminal) or use something equivalent like Postman

`curl -F “url=<ngrok_url>/c817304a3d163ebd58b44dd446eba29572300724098cdbca1a/“ https://api.telegram.org/bot<bot_token>/setWebhook`

