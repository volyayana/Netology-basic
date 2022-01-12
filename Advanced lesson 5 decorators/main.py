import datetime
import os
import requests

LOG_FILE = os.path.join(os.getcwd(), 'log.csv')

def log_decor_param(log_path):
    def log_decor(old_function):
        def new_function(*args, **kwargs):
            exec_time = datetime.datetime.now()
            result = old_function(*args, **kwargs)
            with open(log_path, 'a', encoding='UTF-8') as f:
                if os.stat(log_path).st_size == 0:
                    f.writelines('exec_date;function_name;args;kwargs;function_result\n')
                f.writelines(f'{exec_time};{old_function.__name__};{args};{kwargs};{result}\n')
            return result
        return new_function
    return log_decor

@log_decor_param(LOG_FILE)
def get_smartest_hero(*hero_list):
    hero_dict_list = []
    for hero in hero_list:
        r = requests.get(f'https://superheroapi.com/api/2619421814940190/search/{hero}').json()
        hero_dict_list.append({'name': r['results'][0]['name'], 'intelligence': int(r['results'][0]['powerstats']['intelligence'])})
    return f'Самый умный герой - {max(hero_dict_list, key=lambda k: k["intelligence"])["name"]}'

print(get_smartest_hero('hulk', 'captain america', 'thanos'))