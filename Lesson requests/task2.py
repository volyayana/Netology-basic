import os
import requests

class YaUploader:
    def __init__(self):
        self.token = self.get_token()
        self.headers = {
            'Accept': 'application/json',
            'Authorization': 'OAuth ' + self.token
        }

    def get_token(self):
        with open(os.path.join(os.getcwd(), 'yatoken.txt'), 'r') as file_object:
            token = file_object.read().strip()
        return token

    def upload(self, file_path: str):
        # Получение ссылки для загрузки файла
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {
            'path': os.path.basename(file_path),
            'url': url
        }
        result = requests.get(url, params=params, headers = self.headers).json()

        # Загрузка файла по полученной ссылке
        result_upload = requests.put(result['href'], data=open(file_path))


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = os.path.join(os.getcwd(), 'test1.txt')
    uploader = YaUploader()
    result = uploader.upload(path_to_file)