import httpx as requests
import pystyle
import threading
import time
import sys
from plugins.configuration.load import config

class smshubverification:
    def __init__(self):
        # CAPTCHASERVICE, CAPTCHAAPI, CAPTCHASITEKEY, PHONESERVICE, RETRIES, self.OPERATOR, VAKSMSAPI, VAKSMSCOUNTRY, FIVESIMAPI, FIVESIMCOUNTRY, SMSHUBAPI, SMSHUBCOUNTRY, WEBHOOK = config().loadconfig()
        
        _, _, _, _, self.OPERATOR, _, _, _, _, _, self.APIKEY, self.COUNTRY, _ = config().loadconfig()
        self.BALANCE = None
        self.STOCK = None
        self.PRICE = None
        self.NUMBER = None
        self.TZID = None
        self.VERIFYCODE = None
        self.BANNED = False
        self.DELETED = False
        self.TIMEOUT = requests.Timeout(20.0, read=None)
    

    def ordernumber(self):
        url = f"https://smshub.org/stubs/handler_api.php?api_key={self.APIKEY}&action=getNumber&service=ds&operator={self.OPERATOR}&country={self.COUNTRY}"
        with requests.Client() as client: response = client.get(url)
        
        def smshub_internal_error_handle(self):
            if "BAD_KEY" in response.text:
                pystyle.Write.Print(f"\t[*] Could not order the Number (API Key is Invalid)!\n", pystyle.Colors.yellow, interval=0)
                sys.exit(1)
            
            elif "BAD_SERVICE" in response.text:
                pystyle.Write.Print(f"\t[*] Could not order the Number (Service Name is Incorrect)!\n", pystyle.Colors.yellow, interval=0)
                sys.exit(1)
            
            elif "BAD_ACTION" in response.text:
                pystyle.Write.Print(f"\t[*] Could not order the Number (General query is malformed)!\n", pystyle.Colors.yellow, interval=0)
                sys.exit(1)
            
            elif "ERROR_SQL" in response.text:
                pystyle.Write.Print(f"\t[*] Could not order the Number (SQL Server Database Error)!\n", pystyle.Colors.yellow, interval=0)
                sys.exit(1)
        smshub_internal_error_handle(self)
        

        def smshub_user_error_handle(self):
            if "NO_NUMBERS" in response.text:
                pystyle.Write.Print(f"\t[*] Could not order the Number (No Numbers with the specified parameters aviable)!\n", pystyle.Colors.yellow, interval=0)
                sys.exit(1)
            
            elif "NO_BALANCE" in response.text:
                pystyle.Write.Print(f"\t[*] Could not order the Number (Not enough Funds)!\n", pystyle.Colors.yellow, interval=0)
                sys.exit(1)
            
            elif "WRONG_SERVICE" in response.text:
                pystyle.Write.Print(f"\t[*] Could not order the Number (Invalid service identifier)!\n", pystyle.Colors.yellow, interval=0)
                sys.exit(1)
        smshub_user_error_handle(self)
        
        if ":" in response.text:
            _, self.TZID, self.NUMBER = response.text.split(':')
        
        return self.NUMBER, self.TZID
    

    def deletenumber(self):
        url = f"https://smshub.org/stubs/handler_api.php?api_key={self.APIKEY}&action=setStatus&status=8&id={self.TZID}"
        requests.get(url)
    

    def getcode(self):
        waitcount = 0
        url = f"https://smshub.org/stubs/handler_api.php?api_key={self.APIKEY}&action=getStatus&id={self.TZID}"
        discordurl = "https://discord.com/api/v9/users/@me/phone"
        with requests.Client() as client: response = client.get(url)
        
        def smshub_internal_error_handle(self):
            if "BAD_KEY" in response.text:
                pystyle.Write.Print(f"\t[*] Could get the SMS Code (API Key is Invalid)!\n", pystyle.Colors.yellow, interval=0)
                sys.exit(1)
            
            elif "BAD_SERVICE" in response.text:
                pystyle.Write.Print(f"\t[*] Could get the SMS Code (Service Name is Incorrect)!\n", pystyle.Colors.yellow, interval=0)
                sys.exit(1)
            
            elif "BAD_ACTION" in response.text:
                pystyle.Write.Print(f"\t[*] Could get the SMS Code (General query is malformed)!\n", pystyle.Colors.yellow, interval=0)
                sys.exit(1)
            
            elif "ERROR_SQL" in response.text:
                pystyle.Write.Print(f"\t[*] Could get the SMS Code (SQL Server Database Error)!\n", pystyle.Colors.yellow, interval=0)
                sys.exit(1)
        smshub_internal_error_handle(self)

        while response.text == "STATUS_WAIT_CODE": 
            waitcount += 1

            pystyle.Write.Print(f"\t[*] Discord haven't sent the SMS so far... {waitcount}/120!\n", pystyle.Colors.yellow, interval=0)
            with requests.Client(timeout=self.TIMEOUT) as client:
                response = client.get(url)
                time.sleep(.3)
            
            if waitcount >= 120:
                return "TIMEOUT", False
        
        if ":" in response.text: self.VERIFYCODE = response.text.split(":")[1]
        return waitcount, self.VERIFYCODE
