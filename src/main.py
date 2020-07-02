from bs4 import BeautifulSoup
from src import logging
import argparse
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
    logger.info("Bought item {} successfully.".format(str(itemid)))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', action='store', dest='username')
    parser.add_argument('--password', action='store', dest='password')
    parser.add_argument('--itemid', action='store', dest='itemid')
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    logger = logging.Logger(__name__)
    s = get_session(args.username, args.password)
    purchase_item(s, args.itemid)
    sys.exit(0)
