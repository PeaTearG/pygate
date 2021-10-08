import requests
try:
    from . import functions
except:
    import functions
from datetime import datetime

class Environment:

    def __init__(self, data):
        self.data = data
        for k, v in self.data.items():
            setattr(self, k, v)
        self.auth_body = {"deviceId": self.deviceId,
                          "providerName": self.providerName,
                          "username": self.username,
                          "password": self.password
                          }
class Controller():
    _base = "https://{}:8443/admin/"
    _search = "https://{}:8443/auditlogs/"
    product = "SDP"

    def __init__(self, collective):
        self.collective = collective
        self.environment = Environment(functions.get(Controller.product, collective))
        self.baseurl = Controller._base.format(self.environment.url)
        self.searchurl = Controller._search.format(self.environment.url)
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/vnd.appgate.peer-v10+json"})
        self.session.verify = self.environment.controller_ssl_root if self.environment.controller_ssl_root else True
        self.token = ""
        self.token_expires = ""


    def auth(self):
        login_url = self.baseurl + "login"
        if "Authorization" in self.session.headers:
            resp = self.session.post(login_url, json=self.environment.auth_body, headers={'Authorization': None})
        else:
            resp = self.session.post(login_url, json=self.environment.auth_body)
        return resp

    def token_handler(self):
        if self.token and self.not_expired():
            print('token is present and is not expired, aka that shit is valid')
            pass
        else:
            print('getting a new token')
            auth_resp = self.auth()
            auth_data = functions.httpcheckandreturn(auth_resp)
            self.token = auth_data['token']
            self.token_expires = auth_data['expires']
            self.update_headers()

    def update_headers(self):
        headers = {"Authorization": "Bearer " + self.token}
        self.session.headers.update(headers)

    def not_expired(self):
        if datetime.fromisoformat(self.token_expires[:-1]) > datetime.now():
            return True
        else:
            return False

    def active_sessions(self, query):
        self.token_handler()
        url = self.baseurl + "stats/active-sessions"
        params = {
            "orderBy": "username",
            "descending": False,
            "query": query}
        resp = self.session.get(url, params=params)
        return functions.httpcheckandreturn(resp)

    def appliance_stats(self):
        self.token_handler()
        url = self.baseurl + "stats/appliances"
        resp = self.session.get(url)
        return functions.httpcheckandreturn(resp)

    def custom_get(self, resource):
        self.token_handler()
        url = self.baseurl + resource
        resp = self.session.get(url)
        return functions.httpcheckandreturn(resp)

    def custom_post(self, resource, body):
        self.token_handler()
        url = self.baseurl + resource
        resp = self.session.post(url,
                                 json=body)
        return functions.httpcheckandreturn(resp)

    def custom_del(self, resource, params):
        self.token_handler()
        url = self.baseurl + resource
        resp = self.session.delete(url,
                                   params=params)
        return functions.httpcheckandreturn(resp)

    def custom_put(self, resource, body):
        self.token_handler()
        url = self.baseurl + resource
        resp = self.session.put(url,
                                json=body)
        return functions.httpcheckandreturn(resp)

    def audit_logs(self, resource):
        self.token_handler()
        url = self.baseurl + resource
        resp = self.session.get(url)
        return functions.httpcheckandreturn(resp)


