
from api import PetFriends
from settings import valid_email, valid_password, invalid_email
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='КОТЭ', animal_type='двортерьер',
                                     age='3', pet_photo='images/Cats.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_successful_pet_created(name='Мурзик', animal_type='КОТЯРА', age='3'):
    """Проверяет возможность создать питомца без фотографии"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_a_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_cannot_add_a_pet_with_blanc_name_type_age(name='', animal_type='', age=''):
    """Проверяет невозможность создать питомца с незаполненными обязательными
    параметрами: имя, тип, возраст"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_a_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 400


def test_cannot_add_a_pet_with_invalid_age(name='кошка', animal_type='cat', age='-5'):
    """Проверяет невозможность создать питомца с отрицательным возрастом"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_a_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 400


def test_cannot_add_pet_with_invalid_age(name='Васька', animal_type='cat', age='hjd'):
    """Проверяет невозможность создать питомца с символами вместо возраста"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_a_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 400


def test_add_photo_to_existing_pet_successfully(pet_photo='images/Cats.jpg'):
    """Добавляет или обновляет фотографию существующему питомцу."""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_to_existing_pet(auth_key, pet_id, pet_photo)

    assert status == 200
    assert len(result['pet_photo']) > 0


def test_cannot_add_text_file_as_existing_pet_photo(pet_photo='images/1.txt'):
    """Невозможно добавить текстовый файл вместо фото существующему питомцу."""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_to_existing_pet(auth_key, pet_id, pet_photo)

    assert status == 400


def test_cannot_get_api_key_invalid_email(email=invalid_email, password=valid_password):
    """Проверяем получение апи ключа для невалидного email"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_cannot_get_api_key_invalid_password(email=invalid_email, password=""):
    """Проверяем получение апи ключа для отсутствующего пароля"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_cannot_get_all_pets_with_invalid_filter(filter='asdf'):
    """Проверяем, что при запросе списка питомцев с невалидным фильтром
    выходит ошибка 400 (некорректный запрос)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 400



def test_cannot_delete_pet_with_invalid_id():
    """Проверяем невозможность удалить питомца с несуществующим id: создаём питомца и два раза его удаляем"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/Cats.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    status, _ = pf.delete_pet(auth_key, pet_id)

    assert status == 400
