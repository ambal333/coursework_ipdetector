import requests
import json
import os
from api_key import API_KEY
from API_KEY_IP import api_key_ip
class Detector:
    folder='result.json'
    file='ip_info.json'
    yandex_url='https://cloud-api.yandex.net/v1/disk/resources'
    def __init__(self,group_number,api_key_yandex,api_key_ipinfo):
        self.group_number=group_number
        self.api_key_yandex=api_key_yandex
        self.api_key_ipinfo=api_key_ipinfo
    @staticmethod
    def __get_ip():
        params={'format':'json'}
        url='https://api.ipify.org/'
        response=requests.get(url,params=params)
        data=response.json()
        return data.get('ip')
    def get_city(self):
        url='https://ipinfo.io/'
        params={'token':self.api_key_ipinfo}
        response=requests.get(f'{url}{self.__get_ip()}/geo')
        data=response.json()
        return data
    def json_create(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder,exist_ok=True)
        else:
            print(f'папка {self.folder} уже существует')
        with open(f'{self.folder}/{self.file}','w',encoding='utf-8') as f:
            json.dump(self.get_city(),f,ensure_ascii=False,indent=2)
        print( f'файл json создан в папке {self.folder}')
    def create_folder_yandexdisc(self):
        self.json_create()
        params={'path':self.group_number}
        headers={'Authorization':f'OAuth {self.api_key_yandex}' }
        response=requests.put(self.yandex_url,params=params,headers=headers)
        print('папка в яндекс диске создана')
        
    def get_yandex_link(self):
        params={'path':f'{self.group_number}/{self.file}','overwrite':'true'}
        headers={'Authorization':f'OAuth {self.api_key_yandex}' }
        response=requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',headers=headers,params=params)
        data = response.json()
        result = data.get('href')
        return result
    def send_file_yandex(self):
        params={'path':self.group_number}
        with open(f'{self.folder}/{self.file}',encoding='utf-8') as f: 
            response=requests.put(self.get_yandex_link(),files={'file':f})
        return 'файл добавлен'

ip = Detector('IP_PY-254','y0__wgBEIjItOADGNuWAyCRkfH2FxMP-fVDRx12Ugn7xPvrKl3428D4','54dbcf15770003')
ip.create_folder_yandexdisc()
res=ip.send_file_yandex()
print(res)