from vkontakte import VK
from vk_api.longpoll import VkEventType


vk = VK()
last_request =''

for event in vk.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request.lower() == "привет":
                vk.write_msg(event.user_id, f"Привет, {vk.get_user_name(event.user_id)}")

                vk.write_msg(event.user_id, f"Введи критерии поиска: \nгород (и страна, если город не в России), \nпол,"
                                            f"\nсемейное положение, \nвозраст с, \nвозраст до. "
                                            f"\n\nПример: 'город: Пластуновская, семейное положение: женат'"
                                            f"\n\nДополнительные команды:"
                                            f"\n    добавь в белый список"
                                            f"\n    покажи белый список"
                                            f"\n    далее")
            elif request.lower() == "подробнее" or request.lower() == "справка":
                vk.write_msg(event.user_id, f"Возможные значения: \nПол: {list(vk.sex.keys())}"
                                            f"\nСемейное положение: {list(vk.status.keys())}")
            elif request.lower() == "добавь в белый список":
                vk.add_to_white_list(event.user_id)
                vk.write_msg(event.user_id, 'Добавление в белый список успешно выполнено')
            elif request.lower() == "покажи белый список":
                print(vk.get_white_list(event.user_id))
            elif request.lower() == "далее":
                if last_request != '':
                    input_parameters = vk.parse_parameters(last_request)
                    found_user = vk.search_users(event.user_id, **input_parameters)
                    if found_user == -1:
                        vk.write_msg(event.user_id, "Пользователи по указанным критериям не найдены")
                        break
                    photo_array = vk.get_photos(found_user)
                    vk.send_photos(event.user_id, photo_array)
                else:
                    vk.write_msg(event.user_id, "Ранее не были введены критерии поиска")

            for key in vk.parameters_dict.keys():
                if key in request.lower():
                    last_request = request.lower()
                    input_parameters = vk.parse_parameters(request.lower())
                    found_user = vk.search_users(event.user_id, **input_parameters)
                    if found_user == -1:
                        vk.write_msg(event.user_id, "Пользователи по указанным критериям не найдены")
                        break
                    photo_array = vk.get_photos(found_user)
                    vk.send_photos(event.user_id, photo_array)
                    break
