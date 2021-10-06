import requests

def get_smartest_hero(*hero_list):
    hero_dict_list = []
    for hero in hero_list:
        r = requests.get(f'https://superheroapi.com/api/2619421814940190/search/{hero}').json()
        hero_dict_list.append({'name': r['results'][0]['name'], 'intelligence': int(r['results'][0]['powerstats']['intelligence'])})
    return f'Самый умный герой - {max(hero_dict_list, key=lambda k: k["intelligence"])["name"]}'


print(get_smartest_hero('hulk', 'captain america', 'thanos'))
