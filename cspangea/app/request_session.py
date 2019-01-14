#!/usr/bin/python
import requests
from bs4 import BeautifulSoup

from cspangea.app.constants import HOME_TITLE


def get_cookie() -> requests.sessions.Session:
    print("Generando cookie de acceso...")
    with requests.Session() as s:
        s.post("http://desarrollo.lda/CheckingPRO/j_acegi_security_check",
               data={
                   "j_username": "INTERNET",
                   "j_role": "ROLE_DEVELOPER",
                   "j_password": "INTERNET"})
    return s


def validate_access(s: requests.sessions.Session) -> bool:
    base_page = s.get('http://desarrollo.lda/CheckingPRO/dashboard/view.run?category=requests')
    try:
        soup = BeautifulSoup(base_page.content, 'html.parser')

        if HOME_TITLE == soup.title.get_text():
            print("Acceso verificado.")
            return True

        else:
            print("No se ha logrado acceder.")

    except Exception as e:
        print("error de acceso", e)

    return False
