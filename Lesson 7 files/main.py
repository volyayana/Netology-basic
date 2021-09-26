import os
from pprint import pprint

def get_recipes_data(file_name):

    recipes = {}
    with open(os.path.join(os.getcwd(), file_name), encoding='utf-8') as file:
        for dish in file:
            temp_list = []
            dish_name = dish.strip()
            ingredient_count = int(file.readline().strip())

            for i in range(ingredient_count):
                ingredient_name, quantity, measure = file.readline().strip().split(' | ')
                temp_list.append({'ingredient_name': ingredient_name, 'quantity': int(quantity), 'measure': measure})

            file.readline()
            recipes[dish_name] = temp_list
    
    return recipes
            
def get_shop_list_by_dishes(dishes, person_count):
    recipes = get_recipes_data('recipes.txt')

    ingredient_list = {}
    for recipe, ingredients in recipes.items():
        if recipe in dishes:
            for ingredient in ingredients:
                if ingredient['ingredient_name'] in ingredient_list.keys():
                    ingredient_list[ingredient['ingredient_name']]['quantity'] += ingredient['quantity'] * person_count
                else:
                    ingredient_list[ingredient['ingredient_name']] = {'measure': ingredient['measure'], 'quantity': ingredient['quantity'] * person_count}
    return ingredient_list
            


def prepare_file(file_name):
    with open(os.path.join(os.getcwd(), file_name), encoding='utf-8') as file:
        content = file.read()
        return {'name': file_name, 'len': len(content.split('\n')), 'content': content}

def concat_files(file_list, out_file_name):
    file_dicts = []
    for in_file in file_list:
        file_dicts.append(prepare_file(in_file))
    sorted_file_list = sorted(file_dicts, key = lambda k: k['len'])

    with open(os.path.join(os.getcwd(), out_file_name), 'w', encoding='utf-8') as out_file:
        for sorted_file in sorted_file_list:
            out_file.writelines(f'{sorted_file["name"]}\n{sorted_file["len"]}\n{sorted_file["content"]}\n')




#pprint(get_recipes_data('recipes.txt'))
pprint(get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2))
#print(prepare_file('1.txt'))
concat_files(['1.txt', '2.txt', '3.txt'], 'new_file.txt')