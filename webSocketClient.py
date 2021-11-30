import websocket
import json
import time
import base64
import hmac
import hashlib
from config import api_secret, api_key, api_pass

class WebSocketClient:
    def __init__(self):
        #sandbox: 'wss://ws-feed-public.sandbox.pro.coinbase.com'
        #pro: 'wss://ws-feed.exchange.coinbase.com'
        self.url = ''
        self.key = api_key
        self.passkey = api_pass
        self.secret = api_secret
        self.open = False
        self.auth = False
        self.products = []
        self.params = {}
        self.count = 0
        self.ws = None

        if api_secret != '' and api_key != '' and api_pass != '':
            self.auth = True
        
        if self.products == []:
            self.products = ["BTC-USD"]

        if self.params == {}:
            self.params = {"type": "subscribe","product_ids": self.products,"channels": ["ticker"]}


    def connect(self):
        if self.open:
            raise Exception('Connection already established')
        
        self.open = not(self.open)

        if self.auth:
            timestamp = str(time.time())
            msg = timestamp + 'GET' + '/users/self/verify'
            msg = msg.encode('ascii')
            key = base64.b64decode(self.secret)
            signature = hmac.new(key,msg,hashlib.sha256)
            signature = base64.b64encode(signature.digest()).decode('utf-8')
            self.params['signature'] = signature
            self.params['key'] = self.key
            self.params['passphrase'] = self.passkey
            self.params['timestamp'] = timestamp

        self.ws = websocket.create_connection(self.url)
        self.ws.send(json.dumps(self.params))
        

    def stream(self):
        if self.open:
            data = self.ws.recv()
            print(json.loads(data))
            self.count += 1
            time.sleep(4)

    def close(self):
        self.open = not(self.open)
        data = self.ws.recv()
        print(json.loads(data))
        self.ws.close()
        self.count += 1
        print('Total messages recieved: {}'.format(self.count))
