import re
import datetime
import vk_api
import os
from random import randrange
from vk_api.longpoll import VkLongPoll
from database import Database


class VK:
    parameters_dict = {'страна': 'country',
                            'город': 'city',
                            'пол': 'sex',
                            'семейное положение': 'status',
                            'возраст с': 'age_from',
                            'возраст до': 'age_to'}
    sex = {'женский': 1, 'мужской': 2}
    status = {'не женат': 1,
              'не замужем': 1,
              'холост': 1,
              'встречается': 2,
              'помолвлен': 3,
              'женат': 4,
              'замужем': 4,
              'все сложно': 5,
              'всё сложно': 5,
              'в активном поиске': 6,
              'влюблен': 7,
              'влюблена': 7,
              'в гражданском браке': 8}

    def __init__(self):
        with open(os.path.join(os.getcwd(), 'vktoken_post.txt'), 'r') as file_object:
            token_club = file_object.read().strip()
        with open(os.path.join(os.getcwd(), 'vktoken_get.txt'), 'r') as file_object:
            token_user = file_object.read().strip()

        self.vk_club = vk_api.VkApi(token=token_club)
        self.vk_user = vk_api.VkApi(token=token_user)
        self.longpoll = VkLongPoll(self.vk_club)
        self.db = Database()
        self.offset = 1

    def log_decor(old_function):
        def new_function(*args, **kwargs):
            exec_time = datetime.datetime.now()
            result = old_function(*args, **kwargs)
            func_name = str(old_function)
            func_name = func_name[1 : func_name.find(' at ')]
            args[0].db.add_logs(args[1], func_name, exec_time)
            return result
        return new_function

    def parse_parameters(self, input_params):
        out_parameters = {}
        for parameters in input_params.lower().split(','):
            parameters_list = parameters.strip().split(':')
            parameter_name = self.parameters_dict[parameters_list[0]]
            if parameter_name == 'sex':
                parameter_value = self.sex[parameters_list[1].strip()]
            elif parameter_name == 'status':
                parameter_value = self.status[parameters_list[1].strip()]
            else:
                parameter_value = parameters_list[1].strip()
            out_parameters[parameter_name] = parameter_value
        print(out_parameters)
        return out_parameters

    @log_decor
    def get_user_name(self, user_id):
        return self.vk_user.method('users.get', {'v': '5.131', 'user_ids': user_id})[0]['first_name']

    # токен пользователя
    @log_decor
    def search_users(self, user_id, age_from='', age_to='', sex='', city='', country='Россия', status=''):
        # Обращаемся в БД, чтобы сократить количество обращений к API
        country_id = self.db.get_country(country)
        city_id = self.db.get_city(city, country_id)
        if city_id is None:
            in_city = self.vk_user.method('database.getCities', {'v': '5.131', 'q': city, 'country_id': country_id})
            if in_city['count'] > 0:
                city_id = in_city['items'][0]['id']
                self.db.add_city(in_city['items'][0]['id'], in_city['items'][0]['title'], country_id)
            else:
                city_id = None
        users = self.vk_user.method('users.search', {'v': '5.131', 'age_from': age_from, 'age_to': age_to, 'sex': sex,
                                                     'city': city_id, 'status': status, 'offset': self.offset})
        if len(users['items']) == 0:
            print("Пользователи не найдены")
            return -1
        print(users['items'][0]['first_name'], users['items'][0]['last_name'])
        self. offset += 1
        found_user_id = users['items'][0]['id']
        # Добавляем в БД найденного пользователя, чтобы исключить его в будущем
        if self.db.check_found_users(user_id, found_user_id) == 0:
            self.db.add_found_users(user_id, found_user_id)
        else:
            return self.search_users(user_id, age_from=age_from, age_to=age_to, sex=sex, city=city, country=country,
                                     status=status)
        # борьба с закрытыми аккаунтами
        if users['items'][0]['is_closed']:
            return self.search_users(user_id, age_from=age_from, age_to=age_to, sex=sex, city=city, country=country,
                                     status=status)
        else:
            return found_user_id

    # токен пользователя
    @log_decor
    def get_photos(self, user_id):
        print(user_id)
        photos = self.vk_user.method('photos.get', {'v': '5.131', 'owner_id': user_id, 'album_id': 'profile',
                                                    'extended': 1})['items']
        photos.extend(self.vk_user.method('photos.getUserPhotos', {'v': '5.131', 'owner_id': user_id,
                                                                   'extended': 1})['items'])
        result_photo_array = []
        for photo in photos:
            likes_count = photo['likes']['count']
            comments_count = photo['comments']['count']
            popularity = likes_count + comments_count
            result_photo_array.append({'user_id': user_id, 'id': photo['id'], 'owner_id': photo['owner_id'],
                                       'popularity': popularity, 'message': ''})

        result_photo_array = sorted(result_photo_array, key=lambda user: user['popularity'], reverse=True)
    #    print(result_photo_array)
        if len(result_photo_array) == 0:
            return [{'user_id': user_id, 'message': 'Фотографий нет'}]
        return result_photo_array[0:3]

    # токен сообщества
    @log_decor
    def send_photos(self, user_id, photo_array):
        attachment = ''
        if photo_array[0]["message"] == '':
            for photo in photo_array:
                attachment += f'photo{photo["owner_id"]}_{photo["id"]},'
        self.vk_club.method('messages.send',
            {'v': '5.131',
             'user_id': user_id,
             'random_id': randrange(10 ** 7),
             'message': f'https://vk.com/id{photo_array[0]["user_id"]} \n{photo_array[0]["message"]}',
             'attachment': attachment}
        )

    @log_decor
    def add_to_white_list(self, user_id):
        messages = self.vk_club.method('messages.getHistory', {'v': '5.131', 'user_id': user_id, 'count': 2})['items']
        white_user_id = re.findall('[0-9]+', messages[-1]['text'])[0]
        print(white_user_id)
        self.db.add_to_white_list(user_id, white_user_id)

    @log_decor
    def get_white_list(self, user_id):
        white_list_users = self.db.get_white_list(user_id)
        for white_user in white_list_users:
            photo_array = self.get_photos(white_user[0])
            self.send_photos(user_id, photo_array)

    @log_decor
    def write_msg(self, user_id, message):
        self.vk_club.method('messages.send', {'user_id': user_id, 'message': message,
                                              'random_id': randrange(10 ** 7),})