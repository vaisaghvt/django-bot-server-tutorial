import json
from channels import Channel
from channels.auth import channel_session_user_from_http, channel_session_user
from channels.sessions import channel_session, enforce_ordering

from datetime import timedelta
from .views import respond_to_websockets
# WebSocket handling ###


# This decorator copies the user from the HTTP session (only available in
# websocket.connect or http.request messages) to the channel session (available
# in all consumers with the same reply_channel, so all three here)
@enforce_ordering
def ws_connect(message):
    # Initialise their session
    message.reply_channel.send({
        'accept': True
    })


# Unpacks the JSON in the received WebSocket frame and puts it onto a channel
# of its own with a few attributes extra so we can route it
# This doesn't need @channel_session_user as the next consumer will have that,
# and we preserve message.reply_channel (which that's based on)
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

# Channel_session_user loads the user out from the channel session and presents
# it as message.user. There's also a http_session_user if you want to do this
# on a low-level HTTP handler, or just channel_session if all you want is the
# message.channel_session object without the auth fetching overhead.
# THis function is called when the user starts chatting for a particular job.
@channel_session_user
def chat_start(message):
	pass
        # sgt_creation_time = im.created_at + timedelta(
        #     seconds=8 * 60 * 60)
        # message_to_send = {
        #     'content': im.display_message(),
        #     'source': im.source,
        #     'init_message': True,
        #     'time': sgt_creation_time.strftime(
        #         "%d %b, %I:%M %p (SGT)")
        # }
        # last_im = message_to_send
        # message.reply_channel.send({
        #     'text': json.dumps(message_to_send)
        # })


@channel_session_user
def chat_leave(message):
    # Reverse of join - remove them from everything.
    # if user logged in:
    #   find the current room with job id and user id
    #   remove the room_id from the list for this channel
    #   remove this reply_channel from the group associated with the room

    pass


@channel_session_user
def chat_send(message):
    # if int(message['room']) not in message.channel_session['rooms']:
    #     raise ClientError("ROOM_ACCESS_DENIED")

    message_to_send_content = {
        'text': message['text'],
        'type': 'text', 
        'source': 'CANDIDATE'
    }
    message.reply_channel.send({
    	'text':json.dumps(message_to_send_content)
    })
    
    response = respond_to_websockets(
    	message
    )
    response['source'] = 'BOT'
    message.reply_channel.send(
    	{'text':json.dumps(response)}
    )

