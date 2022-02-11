from random import randrange
import os
import sqlalchemy

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

with open(os.path.join(os.getcwd(), 'vktoken_post.txt'), 'r') as file_object:
    token_club = file_object.read().strip()
with open(os.path.join(os.getcwd(), 'vktoken_get.txt'), 'r') as file_object:
    token_user = file_object.read().strip()
#token = input('Token: ')

class Database():
    def __init__(self):
        self.engine = sqlalchemy.create_engine('postgresql://netol:1111@localhost:5432/netol_db')
        self.connection = self.engine.connect()

    def get_country(self, name):
        return self.connection.execute(
            f"SELECT max(id)"
            f"  FROM countries c"
            f" WHERE lower(c.name) like lower('%%{name}%%');"
        ).fetchall()[0][0];

    def get_city(self, name, country_id):
        return self.connection.execute(
            f"SELECT max(id)"
            f"  FROM cities c"
            f" WHERE lower(c.name) like lower('%%{name}%%')"
            f"   AND country_id = {country_id};"
        ).fetchall()[0][0];

    def add_city(self, id, name, country_id):
        return self.connection.execute(
            f"INSERT INTO cities(id, name, country_id)"
            f"VALUES ({id}, '{name}', {country_id});"
        )

    def add_found_users(self, user_id, found_user_id):
        return self.connection.execute(
            f"INSERT INTO found_users(user_id, found_user_id) "
            f"VALUES ('{user_id}', {found_user_id});"
        )

    def check_found_users(self, user_id, found_user_id):
        return self.connection.execute(
            f"SELECT COUNT(*)"
            f"  FROM found_users fu"
            f" WHERE fu.user_id = {user_id}"
            f"   AND fu.found_user_id = {found_user_id};"
        ).fetchall()[0][0]



class VK():
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
        self.vk_club = vk_api.VkApi(token=token_club)
        self.vk_user = vk_api.VkApi(token=token_user)
        self.longpoll = VkLongPoll(self.vk_club)
        self.db = Database()
        self.offset = 1


    def parse_parameters(self, input):
        out_parameters = {}
        for parameters in input.lower().split(','):
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

    # токен пользователя
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
        users = self.vk_user.method('users.search', {'v': '5.131', 'age_from': age_from, 'age_to': age_to, 'sex': sex, 'city': city_id,
          'status': status, 'offset': self.offset})
        print(users)
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
    def get_photos(self, user_id):
        print(user_id)
        photos = self.vk_user.method('photos.get', {'v': '5.131', 'owner_id': user_id, 'album_id': 'profile',
                                                    'extended': 1})['items']
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
    def send_photos(self, photo_array, user_id):
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


    def write_msg(self, user_id, message):
        self.vk_club.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


vk = VK()

for event in vk.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request.lower() == "привет":
                vk.write_msg(event.user_id, f"Привет!, {event.user_id}")

                vk.write_msg(event.user_id, f"Введи критерии поиска: \nгород (и страна, если город не в России), \nпол, "
                                            f"\nсемейное положение, \nвозраст с, \nвозраст до. \nПример: 'город: Пластуновская, семейное положение: женат'")
            if request.lower() == "подробнее" or request.lower() == "справка":
                vk.write_msg(event.user_id, f"Возможные значения: \nПол: {list(vk.sex.keys())}"
                                            f"\nСемейное положение: {list(vk.status.keys())}")

            for key in vk.parameters_dict.keys():
                if key in request.lower():
                    input_parameters = vk.parse_parameters(request.lower())
                    found_user = vk.search_users(event.user_id, **input_parameters)
                    if found_user == -1:
                        vk.write_msg(event.user_id, "Пользователи по указанным критериям не найдены")
                        break
                    photo_array = vk.get_photos(found_user)
                    vk.send_photos(photo_array, event.user_id)
                    break
            # if request == "пока":
            #     vk.write_msg(event.user_id, "Пока((")
            # else:
            #     vk.write_msg(event.user_id, "Не поняла вашего ответа...")





