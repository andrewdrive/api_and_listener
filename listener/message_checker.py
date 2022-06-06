import json
import time
import requests
from datetime import datetime
from kafka import KafkaConsumer


def my_log_time():
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    return '[' + date_time_str + '] '


time.sleep(10)
print(my_log_time() + '----- Hi, listener starts listening Kafka. -----')
consumer = KafkaConsumer('message_topic', bootstrap_servers=['kafka:9092'])


class Listener:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.access_token = None
        self.refresh_token = None

    def get_tokens(self):
        token_url = 'http://api:8000/api/token/'
        auth_data = {'username': self.username, 'password': self.password}
        
        try: 
            response = requests.post(url=token_url, json=auth_data)
        except ConnectionError:
            print(my_log_time() + 'Connection refused cause not existing admin (superuser)')
        if response.status_code == 200:
            self.refresh_token = response.json()['refresh']
            self.access_token = response.json()['access']
            print(my_log_time() + 'Tokens obtained successfully.')
        else:
            print(my_log_time() + str(response.status_code), response.text)

    def verify_token(self):
        verify_url = 'http://api:8000/api/token/verify/'
        data = {'token': self.access_token}
        response = requests.post(url=verify_url, json=data)
        if response.status_code != 200:
            self.access_token = self.refresh_access_token()
            print(my_log_time() + 'JWT was invalid, getting the new one...')
        else:
            print(my_log_time() + 'JWT is valid.')

    def refresh_access_token(self):
        refresh_url = 'http://api:8000/api/token/refresh/'
        data = {'refresh': self.refresh_token}
        response = requests.post(url=refresh_url, json=data)
        if response.status_code == 200:
            print(my_log_time() + 'Got a fresh access token.')
            return response.json()['access']

    @staticmethod
    def message_is_invalid(text):
        forbidden_word = 'АБРАКАДАБРА'
        if forbidden_word.lower() in text.lower():
            return True
        else:
            return False

    def check_and_mark_message(self, mess_id, text):
        success = False
        confirm_url = 'http://api:8000/api/v1/message_confirmation'
        if self.message_is_invalid(text):
            response = requests.post(confirm_url,
                                     json={'message_id': mess_id, 'success': success},
                                     headers={'Authorization': 'Bearer {}'.format(self.access_token)})
            if response.status_code == 200:
                print(my_log_time() + 'Message id={} with text={} marked as Blocked!'.format(mess_id, text))

            elif response.status_code == 401:
                print(my_log_time() + 'Authentication credentials were not provided, Trying again...')
                time.sleep(5)
                self.get_tokens()
                self.verify_token()
                # # # #
                self.check_and_mark_message(mess_id, text)
            else:
                print(my_log_time() + str(response.status_code), response.text)
        else:
            success = True
            response = requests.post(confirm_url,
                                     json={'message_id': mess_id, 'success': success},
                                     headers={'Authorization': 'Bearer {}'.format(self.access_token)})
            if response.status_code == 200:
                print(my_log_time() + 'Message id={} with text={} marked as Correct!'.format(mess_id, text))
            elif response.status_code == 401:
                print(my_log_time() + 'Authentication credentials were not provided, Trying again...')
                time.sleep(5)
                self.get_tokens()
                self.verify_token()
                # # # #
                self.check_and_mark_message(mess_id, text)
            else:
                print(my_log_time() + str(response.status_code), response.text)

    @staticmethod
    def voice():
        print(my_log_time() + "Let's check the messages...")


listener = Listener(username='admin', password='admin')
listener.get_tokens()
listener.verify_token()

while True:
    for message in consumer:
        message_val = json.loads(message.value.decode('utf-8'))
        user_id = message_val['user_id']
        message_id = message_val['message_id']
        text_to_check = message_val['text']
        listener.check_and_mark_message(message_id, text_to_check)
        time.sleep(3)

