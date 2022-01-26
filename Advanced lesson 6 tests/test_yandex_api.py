import requests
import os

class TestYandexApi:
    token = ''
    url = ''
    headers = ''

    @classmethod
    def setup_class(cls):
        with open(os.path.join(os.getcwd(), 'yatoken.txt'), 'r') as file_object:
            yatoken = file_object.read().strip()
        cls.token = yatoken
        cls.url = 'https://cloud-api.yandex.net/v1/disk/resources'
        cls.headers = {
            'Accept': 'application/json',
            'Authorization': 'OAuth ' + cls.token
        }

    def test_success(self):
        params = {
            'path': 'new_folder'
        }
        result = requests.put(self.url, params=params, headers=self.headers)
        assert result.status_code == 201
        result = requests.delete(self.url, params=params, headers=self.headers)
        assert result.status_code == 204
    
    def test_existing_folder(self):
        params = {
            'path': 'new_folder'
        }
        result = requests.put(self.url, params=params, headers=self.headers)
        assert result.status_code == 201
        result = requests.put(self.url, params=params, headers=self.headers)  # дважды создаем одну и ту же папку
        assert result.status_code == 409
        result = requests.delete(self.url, params=params, headers=self.headers)
        assert result.status_code == 204

    def test_wrong_fields(self):
        params = {
            'path': 'new_folder',
            'fields': 'method'
        }
        result = requests.put(self.url, params=params, headers=self.headers).json()['method']
        assert result == 'GET'
        result = requests.delete(self.url, params=params, headers=self.headers)
        assert result.status_code == 204

    def test_long_folder_name(self):
        params = {
            'path': 'lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll'
        }
        result = requests.put(self.url, params=params, headers=self.headers).json()['error']
        assert result == 'DiskNotFoundError'
    
    def test_empty_folder_name(self):
        params = {
            'path': ''
        }
        result = requests.put(self.url, params=params, headers=self.headers).json()['error']
        assert result == 'FieldValidationError'

if __name__ == '__main__':
    test = TestYandexApi()
    test.setup_class()
    test.test_long_folder_name()