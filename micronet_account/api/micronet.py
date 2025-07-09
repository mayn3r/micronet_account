from __future__ import annotations

import re

from httpx import Client
from bs4 import BeautifulSoup

class MicroNET:
    class Auth:
        def __init__(self, micronet: MicroNET):
            self.micronet = micronet
        
        
        def __call__(self, login: str, password: str) -> bool:
            self.micronet._init_cookies()
            
            data = {
                "username": login,
                "password": password,
                "send": ""
            }
            response = self.micronet.client.post("/", data=data)
            
            return response.status_code == 302
        
        
    def __init__(self):
        self.client = Client(base_url="https://cabinet.micronet-rostov.ru/")
        self.client.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"\
                            "Chrome/136.0.0.0 YaBrowser/25.6.0.0 Safari/537.36"
        }
        
        self.auth = self.Auth(self)
        
    
    def _init_cookies(self):
        self.client.get("/")
    
    
    def _get_user_soup(self) -> BeautifulSoup:
        response = self.client.get("user/")
        soup = BeautifulSoup(response.content, "html.parser")
        
        return soup

    
    def balance(self) -> float:
        soup = self._get_user_soup()
        table = soup.find_all("table", class_="table table-striped")[2]
        
        balance = table.find("span").text.strip()
        return float(re.findall("[0-9.]+", balance)[0])

    def status(self) -> str:
        soup = self._get_user_soup()
        table = soup.find_all("table", class_="table table-striped")[2]
        
        status = table.find_all("span")[1].text.strip()
        return status
        
        


if __name__ == "__main__":
    micronet = MicroNET()
    micronet.auth("", "")
    
    print(micronet.balance())
    print(micronet.status())