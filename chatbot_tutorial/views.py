from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse


def get_message_from_request(request):

    received_message = {}
    decoded_request = json.loads(request.body.decode('utf-8'))

    if 'message' in decoded_request:
        received_message = decoded_request['message'] 
        received_message['chat_id'] = received_message['from']['id'] # simply for easier reference

    return received_message


def send_messages(message, token):
    # Ideally process message in some way. For now, let's just respond
    jokes = {
         'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                    """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
         'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                    """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
         'dumb':   ["""THis is fun""",
                    """THis isn't fun"""] 
    }

    post_message_url = "https://api.telegram.org/bot{0}/sendMessage".format(token)

    result_message = {}         # the response needs to contain just a chat_id and text field for  telegram to accept it
    result_message['chat_id'] = message['chat_id']
    if 'fat' in message['text']:
        result_message['text'] = random.choice(jokes['fat'])

    elif 'stupid' in message['text']:
        result_message['text'] = random.choice(jokes['stupid'])

    elif 'dumb' in message['text']:
        result_message['text'] = random.choice(jokes['dumb'])

    else:
        result_message['text'] = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."

    response_msg = json.dumps(result_message)
    status = requests.post(post_message_url, headers={
        "Content-Type": "application/json"}, data=response_msg)


class TelegramBotView(generic.View):

    # csrf_exempt is necessary because the request comes from the Telegram server.
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)


    # Post function to handle messages in whatever format they come
    def post(self, request, *args, **kwargs):
        TELEGRAM_TOKEN = 'WRITE_TOKEN_HERE'
        message = get_message_from_request(request)
        send_messages(message, TELEGRAM_TOKEN)

        return HttpResponse()
