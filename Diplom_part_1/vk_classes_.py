import requests
import datetime
import os
import logging
import json

def get_token():
    with open(os.path.join(os.getcwd(), 'vktoken.txt'), 'r') as file_object:
        vktoken = file_object.read().strip()
    with open(os.path.join(os.getcwd(), 'yatoken.txt'), 'r') as file_object:
        yatoken = file_object.read().strip()
    return vktoken, yatoken

class VKAPI:
    def __init__(self, name_user, token):
        self.token = token  
        
        self.log_file = os.path.join(os.getcwd(), 'export_vk.log')
        self.logger = logging.getLogger("vkapi")
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(self.log_file)
        self.logger.addHandler(fh)

        self.user_id = self.get_id_vk(name_user)

    def get_id_vk(self, name_user):
        self.logger.debug(f'Start get_id_vk {name_user}')
        URL = 'https://api.vk.com/method/users.get'
        params = { 
            'v':'5.130', 
            'access_token': self.token,
            'user_ids': name_user, 
            }
        return requests.get(URL, params=params).json()['response'][0]['id']

    def get_photos(self):
        self.logger.debug(f'Start get_photos user_id={self.user_id}')
        URL = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.user_id,
            'access_token': self.token, # токен и версия api являются обязательными параметрами во всех запросах к vk
            'v':'5.130',
            'album_id': 'profile',
            'extended': 1
        }
        photos = requests.get(URL, params=params).json()['response']['items']
        #print(photos)
        result_photo_array = []
        for photo in photos:
            max_size = 0
            max_photo_size_url = ''
            for size in photo['sizes']:
                # получить url фото максимального размера
                photo_size = size['height'] * size['width']
                if photo_size > max_size:
                    max_size = photo_size
                    max_photo_size_url = size['url']
                    #max_photo_likes = size['url']
            likes_count = photo['likes']['count']
            if likes_count in [j for i in result_photo_array for j in i.values()]:
                file_name = str(likes_count) + '_' + str(datetime.datetime.now().strftime('%H-%M-%S_%d-%m-%Y'))
            else:
                file_name = likes_count
            result_photo_array.append({'url': max_photo_size_url, 'file_name': file_name, 'size': max_size})
        return result_photo_array

class YAAPI():
    def __init__(self, token):
        self.token = token
        #self.vk_fotos_list = vk_fotos_list 
        self.headers = {
            'Accept': 'application/json',
            'Authorization': 'OAuth ' + self.token
        }
        self.result_file = os.path.join(os.getcwd(), 'result_import_yandex')
        
        self.log_file = os.path.join(os.getcwd(), 'import_yandex.log')
        self.logger = logging.getLogger("yaapi")
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(self.log_file)
        self.logger.addHandler(fh)
        

    """Возвращает название директории"""
    def create_folder(self):
        self.logger.debug('Start create_folder')
        folder_name = str(datetime.datetime.now().strftime('%H-%M-%S_%d-%m-%Y'))
        URL = 'https://cloud-api.yandex.net/v1/disk/resources'
        params = {
            'path': folder_name
        }
        result = requests.put(URL, params=params, headers = self.headers)
        #print(result.status_code, folder_name)
        return folder_name

    """
    url - Путь к удаленному ресурсу, ведущий к изображению
    path - директория в ЯД, куда будет загружен файл
    file_name - имя нового файла
    """
    def upload_file(self, url, path, file_name):
        self.logger.debug(f'Start upload_file {path}/{file_name}')
        URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {
            'path': f'{path}/{file_name}.jpg',
            'url': url
        }
        result = requests.post(URL, params=params, headers = self.headers)

    """
    Создает json-файл с результатами
    """
    def create_result_file(self, result):
        with open(self.result_file, 'w', encoding='utf-8') as file:
            file.write(json.dumps(result))

    """
    self.token - токен ЯД
    """
    def upload_photos(self, photo_array, photo_count=5):
        self.logger.debug('Start upload_photos')
        result = []
        sorted_photo_array = sorted(photo_array, key=lambda k: k['size'], reverse=True)
        folder_name = self.create_folder()
        for i in range(min(len(sorted_photo_array), photo_count)):
            self.upload_file(sorted_photo_array[i]['url'], folder_name, sorted_photo_array[i]['file_name'])
            result.append({'file_name': sorted_photo_array[i]['file_name'], 'size': sorted_photo_array[i]['size']})
        #print(result)
        self.create_result_file(result)
        

vktoken, yatoken = get_token()

#забрать фото из VK
vk_instance = VKAPI('begemot_korovin', vktoken)
photos = vk_instance.get_photos()
#print(photos)

#загрузить фото в ЯД
ya_instance = YAAPI(yatoken)
ya_instance.upload_photos(photos, 5)
