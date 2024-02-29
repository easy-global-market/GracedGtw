import requests, json
from requests.auth import AuthBase
from datetime import datetime, timedelta


class AuthError(Exception):
    pass


class BearerAuth(AuthBase):
    "Manage the authentication to the broker, renew it when needed."
    
    def __init__(self, client_id, client_secret, auth_url, auth_scheme='Bearer'):
        self.token = ''
        self.auth_scheme = auth_scheme
        self.client_id = client_id
        self.client_secret = client_secret
        self.client_authurl = auth_url
        self.auth_expire = datetime.now()

    def ensure_auth(self):
        assert(self.client_id)
        assert(self.client_secret)
        assert(self.client_authurl)
        now_time = datetime.now()
        if (now_time < self.auth_expire) :
            return
        r = requests.post(self.client_authurl,
                         data = {
                             "client_id" : self.client_id,
                             "client_secret" : self.client_secret,
                             "grant_type" : "client_credentials"
                             }
                         )

        if (r.status_code != 200):
            print("Error during auth process")
            print(r.text)
            raise AuthError(f"Auth failed : {r.text}",r.status_code)

        self.auth_data = json.loads(r.text)
        self.last_auth = now_time
        self.auth_expire = now_time+timedelta(seconds=int(self.auth_data['expires_in'])-5)
        self.token = self.auth_data["access_token"]

    def __call__(self, request):
        self.ensure_auth()
        request.headers['Authorization'] = f'{self.auth_scheme} {self.token}'
        return request
