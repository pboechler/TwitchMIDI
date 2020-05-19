"""
TwitchMIDI
The following script requires you to have a Twitch account.
A channel which you're gather chat stream data from does not need to be joined.
v1.0 - 05/19/20
"""
server = 'irc.chat.twitch.tv'
port = 6667
nickname = #Enter your Twitch username
token = #Enter your Twitch authorization token "oauth:XXXXXX..."
channel = #Enter the channel name you wish to gather chat data from (always starts with with #)

import socket
import logging
import time
import mido


sock = socket.socket()
sock.connect((server, port))

sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

resp = sock.recv(2048).decode('utf-8')
resp

#Use MIDO to determine your MIDI outputs and then add it to the argument
port = mido.open_output('')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

logging.info(resp)

from emoji import demojize

#This will continue to run until the program is stopped.
#For testing, consider making this a finite loop that will only repeat a set number of times.
while True:
    resp = sock.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))

    elif len(resp) > 0:
        logging.info(demojize(resp))

        # Here is where the MIDI note will be output.
        msg = mido.Message('note_on', note=60, time=2)
        port.send(msg)
