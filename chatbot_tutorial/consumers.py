import json
from channels import Channel
from channels.sessions import enforce_ordering

from .views import respond_to_websockets


@enforce_ordering
def ws_connect(message):
    # Initialise their session
    message.reply_channel.send({
        'accept': True
    })


# Unpacks the JSON in the received WebSocket frame and puts it onto a channel
# of its own with a few attributes extra so we can route it
# we preserve message.reply_channel (which that's based on)
@enforce_ordering
def ws_receive(message):
    # All WebSocket frames have either a text or binary payload; we decode the
    # text part here assuming it's JSON.
    # You could easily build up a basic framework that did this
    # encoding/decoding
    # for you as well as handling common errors.
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("chat.receive").send(payload)


@enforce_ordering
def ws_disconnect(message):
    # Unsubscribe from any connected rooms
    pass


# Chat channel handling ###

def chat_start(message):
    # Genearlly add them to a room, or do other things that should be
    # done when the chat is started
    pass


def chat_leave(message):
    # Reverse of join - remove them from everything.
    # if user logged in:
    #   find the current room with job id and user id
    #   remove the room_id from the list for this channel
    #   remove this reply_channel from the group associated with the room
    pass


def chat_send(message):

    # First send the candidate message in the right format for
    # chatbot to print it on the message channel
    message_to_send_content = {
        'text': message['text'],
        'type': 'text',
        'source': 'CANDIDATE'
    }
    message.reply_channel.send({
        'text': json.dumps(message_to_send_content)
    })

    # Call my view to actually construct the reseponse to
    # the query
    response = respond_to_websockets(
        message
    )

    # Reformat the reponse and send it to the html to print
    response['source'] = 'BOT'
    message.reply_channel.send({
        'text': json.dumps(response)
    })
