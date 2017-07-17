class ErrorMsg():
    def __init__(self, msg):
        self.errcode = msg['errcode']
        self.errmsg = msg['errmsg']


class AccessTokenMsg():
    def __init__(self, msg):
        self.access_token = msg['access_token']
        self.expires_in = msg['expires_in']
