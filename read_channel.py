import base64 # this module is used to encode and decode data
import hmac # is a mechanism for message authentication using cryptographic hash functions
import requests
import sys
from datetime import datetime
import hashlib # for taking variable length of bytes and converting it into a fixed length sequence
from pprint import pprint


class PublisherAPI:
    channel_id = ""
    current_action = ""
    key_id = ""
    key_secret = ""
    url = ""
    
    def send_request(self, method, url, content_type = None):
        date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        canonical_request = method + url + date
        canonical_request = canonical_request.encode()
        signature = self.create_signature(canonical_request)
        authorization = "HHMAC; key=%s; signature=%s; date=%s" % (
            self.key_id, signature, date)
        headers = {"Authorization": authorization}
        return requests.request(method, url, headers = headers)

    def create_signature(self, canonical_request):
        key_bytes = base64.b64decode(self.key_secret)
        message = canonical_request
        secret = self.key_secret.encode("utf-8")

        signature = base64.b64encode(hmac.new(key_bytes, message,digestmod=hashlib.sha256).digest()).decode("utf-8")
        return signature

    def read_channel(self):
        method = "GET"
        url = self.url + "%s" % self.channel_id
        return self.send_request(method, url)

    def main(self):
        if self.current_action == "readChannel":
            response = self.read_channel()
        else:
            response = {
                "status_code": 400,
                "response": "{\"errors\":[{\"code\":\"UNKNOWN_COMMAND\"}]}"
            }
        return response


if __name__ == "__main__":
    if not len(sys.argv) > 4:
        print("no or missing arguments")
        exit()

    publisherAPI = PublisherAPI()
    publisherAPI.url = sys.argv[1] + "/channels/"
    publisherAPI.channel_id = sys.argv[2]
    publisherAPI.key_id = sys.argv[3]
    publisherAPI.key_secret = sys.argv[4]
    publisherAPI.current_action = "readChannel"

    response = publisherAPI.main()

    pprint(response.status_code)
    pprint(response.text)
