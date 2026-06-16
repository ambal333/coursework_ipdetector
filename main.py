import requests
import json
import os
# from api_key import API_KEY
# from API_KEY_IP import api_key_ip
class GetIpify:
    @staticmethod
    def get_ip():
        params = {'format': 'json'}
        url = 'https://api.ipify.org/'
        response = requests.get(url, params=params)
        data = response.json()
        return data.get('ip')
class GetIpinfo:
    yandex_url='https://cloud-api.yandex.net/v1/disk/resources'
    def __init__(self,api_key_ipinfo,ip_adress):
        self.api_key_ipinfo=api_key_ipinfo
        self.ip_adress=ip_adress
    def get_city(self):
        url='https://ipinfo.io/'
        params={'token':self.api_key_ipinfo}
        response=requests.get(f'{url}{self.ip_adress}/geo')
        response.raise_for_status()
        data=response.json()
        return data
class CreateFile:
    folder = 'result'
    file = 'ip_info.json'
    def __init__(self,city):
        self.city=city
    def json_create(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder,exist_ok=True)
        else:
            print(f'папка {self.folder} уже существует')
        with open(f'{self.folder}/{self.file}','w',encoding='utf-8') as f:
            json.dump(self.city,f,ensure_ascii=False,indent=2)
        print( f'файл json создан в папке {self.folder}')
    def delete_folder_local(self):
        os.remove(f'{self.folder}/{self.file}')
        os.rmdir(f'{self.folder}')
        print(f'папка {self.folder} удалена')
class YandexDisc:
    yandex_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    def __init__(self,group_number,api_key_yandex,folder,file):
        self.group_number=group_number
        self.api_key_yandex=api_key_yandex
        self.folder=folder
        self.file=file
    def create_folder_yandexdisc(self):
        params = {'path': self.group_number}
        headers = {'Authorization': f'OAuth {self.api_key_yandex}'}
        response = requests.put(self.yandex_url, params=params, headers=headers)
        print('папка в яндекс диске создана')
    def _get_yandex_link(self):
        params = {'path': f'{self.group_number}/{self.file}', 'overwrite': 'true'}
        headers = {'Authorization': f'OAuth {self.api_key_yandex}'}
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', headers=headers, params=params)
        data = response.json()
        result = data.get('href')
        return result
    def send_file_yandex(self):
        try:
            with open(f'{self.folder}/{self.file}', encoding='utf-8') as f:
                response = requests.put(self._get_yandex_link(), files={'file': f})
        except FileNotFoundError as e:
            print(f'Файл не найден: {e}')
        else:
            return 'файл добавлен'
def main():
    ipify=GetIpify()
    ip= ipify.get_ip()
    ipinfo = GetIpinfo(api_key_ip,ip)
    city_info = ipinfo.get_city()
    file=CreateFile(city_info)
    file.json_create()
    yandex = YandexDisc('IP_PY-254',API_KEY,file.folder,file.file)
    yandex.create_folder_yandexdisc()
    res = yandex.send_file_yandex()
    print(res)
    file.delete_folder_local()
if __name__=='__main__':
    main()
