import json
import os
from retry import retry
from pywebpush import webpush, WebPushException
from util import get_secret

VAPID_PRIVATE_KEY = None
VAPID_PUBLIC_KEY = None

@retry(5, 2)
def get_secret(secret_name):
    try:
        with open('/run/secrets/{0}'.format(secret_name), 'r') as secret_file:
            return secret_file.read()
    except IOError:
        return None

if 'SUB_EMAIL' in os.environ:
    SUB_EMAIL = os.environ['SUB_EMAIL']
else:
    SUB_EMAIL = 'example@example.com'
 
try:
    VAPID_PRIVATE_KEY = open('private_key.txt', "r").readline().strip("\n")
except:
    VAPID_PRIVATE_KEY = get_secret('vapid_key_txt').strip("\n")

try:
    VAPID_PUBLIC_KEY = open('public_key.txt', "r").read().strip("\n")
except:
    VAPID_PUBLIC_KEY = get_secret('vapid_public_key_txt').strip("\n")

VAPID_CLAIMS = {
"sub": f"mailto:{SUB_EMAIL}"
}
 
def send_web_push(subscription_information, message_body):
    return webpush(
        subscription_info=subscription_information,
        data=message_body,
        vapid_private_key=VAPID_PRIVATE_KEY,
        vapid_claims=VAPID_CLAIMS
    )

if __name__ == "__main__":
    response = send_web_push(subscription_info, "this is just a test")
    print('completed')