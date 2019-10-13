import time

import socket
import socks

import requests
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller

controller = Controller.from_port(port=9051)


def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5 , "127.0.0.1", 9050, True)
    socket.socket = socks.socksocket


def renew_tor():
    controller.authenticate('my_password')
    controller.signal(Signal.NEWNYM)


def show_my_ip():
    url = "https://httpbin.org/ip"
    r = requests.Session()
    page = r.get(url)
    print(page.content)


for i in range(10):
    renew_tor()
    connectTor()
    show_my_ip()
    time.sleep(10)