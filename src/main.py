from bs4 import BeautifulSoup
from src import logging
import argparse
import datetime
import requests
import sys


SIGNIN_ENDPOINT = "https://shop.ageofmenor.cc/auth/signin"
PURCHASE_ENDPOINT = "https://shop.ageofmenor.cc/mall/purchases/{}"
HOTDEAL_ENDPOINT = "https://shop.ageofmenor.cc/mall/1/hot"
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


def get_correct_hotdeal_id(hotdeals, itemname):
    for titel in hotdeals:
        if titel.lower().__contains__(str(itemname).lower()):
            logger.info("Hotdeal id found: {} - {}".format(titel, hotdeals[titel]))
            return hotdeals[titel]
    logger.error('No hotdeal for {} found.'.format(str(itemname)))
    sys.exit(1)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', action='store', dest='username', required=True)
    parser.add_argument('--password', action='store', dest='password', required=True)
    parser.add_argument('--itemid', action='store', dest='itemid', required=False)
    parser.add_argument('--desired-time', action='store', dest='desired_time', required=True    )
    parser.add_argument('--itemname', action='store', dest='item_name', required=False)
    return parser.parse_args()


def is_desired_time(desired_time):
    while True:
        if str(datetime.datetime.now().strftime('%H:%M:%S.%f')[:-7]) == str(desired_time) or desired_time is None:
            return True
        else:
            logger.info('Waiting for desired time ... ({} != {})'.format(
                datetime.datetime.now().strftime('%H:%M:%S.%f')[:-7], desired_time))


def get_hotdeals(session):
    deals = {}
    r = session.get(HOTDEAL_ENDPOINT)
    soup = BeautifulSoup(r.content, features="html.parser")
    for li in soup.select_one('div#main-item-box-container').contents[1].findAll('li'):
        try:
            id = str(li.contents[1].attrs["action"]).replace('/mall/purchases/', '')
            titel = str(li.contents[1].contents[1].contents[1].contents[0])
            deals[titel] = id
        except:
            pass
    return deals


if __name__ == "__main__":
    args = get_args()
    logger = logging.Logger(__name__)
    s = get_session(username=args.username, password=args.password)
    if is_desired_time(args.desired_time):
        if args.itemid is None:
            if args.item_name is not None:
                d = get_hotdeals(s)
                id = get_correct_hotdeal_id(hotdeals=d, itemname=args.item_name)
                purchase_item(session=s, itemid=id)
            else:
                logger.error("Whether itemid nor itemname was provided.")
                sys.exit(1)
        else:
            purchase_item(session=s, itemid=args.itemid)
            pass
    sys.exit(0)
