from bs4 import BeautifulSoup
from src import logging
import argparse
import datetime
import requests
import sys


SIGNIN_ENDPOINT = "https://shop.ageofmenor.cc/auth/signin"
PURCHASE_ENDPOINT = "https://shop.ageofmenor.cc/mall/purchases/{}"
csrf_data = {
    "csrf_value": None,
    "csrf_name": None
}


def get_session(username, password):
    global csrf
    session = requests.Session()
    r = session.post(SIGNIN_ENDPOINT, {"username": username, "password": password})

    if r.content.__contains__(b'Incorrect username or password.'):
        logger.error("Login failed. Check username and password.")
        sys.exit(1)

    soup = BeautifulSoup(r.content, features="html.parser")
    csrf_data["csrf_value"] = soup.select_one('input[name="csrf_value"]').attrs["value"]
    csrf_data["csrf_name"] = soup.select_one('input[name="csrf_name"]').attrs["value"]
    return session


def purchase_item(session, itemid):
    session.post(PURCHASE_ENDPOINT.format(itemid), csrf_data)
    logger.info('Attempt to buy itemid {}'.format(str(itemid)))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', action='store', dest='username')
    parser.add_argument('--password', action='store', dest='password')
    parser.add_argument('--itemid', action='store', dest='itemid')
    parser.add_argument('--desired-time', action='store', dest='desired_time')
    return parser.parse_args()


def is_desired_time(desired_time):
    while True:
        if str(datetime.datetime.now().strftime('%H:%M:%S.%f')[:-7]) == str(desired_time):
            return True
        else:
            logger.info('Waiting for desired time ... ({} != {})'.format(
                datetime.datetime.now().strftime('%H:%M:%S.%f')[:-7], desired_time))


if __name__ == "__main__":
    args = get_args()
    logger = logging.Logger(__name__)
    s = get_session(username=args.username, password=args.password)
    if is_desired_time(args.desired_time):
        purchase_item(session=s, itemid=args.itemid)
    sys.exit(0)
