from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email
import os

pf = PetFriends()


def test_get_api_key_for_invalid_email(email=invalid_email, password=invalid_password):
    """Проверяем, что запрос api ключа с неверным email возвращает код 403"""
    status, result = pf.get_api_key(email, password)
    assert status == 403  # Сверяем полученный ответ с ожидаемым результатом
    assert 'This user wasn&#x27;t found in database' in result


def test_get_api_key_for_valid_email_and_invalid_password(email=valid_email, password=invalid_password):
    """Проверяем, что запрос api ключа с верным email и неверным password возвращает код 403"""
    status, result = pf.get_api_key(email, password)
    assert status == 403  # Сверяем полученный ответ с ожидаемым результатом
    assert 'This user wasn&#x27;t found in database' in result


def test_get_all_pets_with_invalid_key(filter=''):
    """Проверяем, что запрос всех питомцев с неверным api ключом возвращает код 403"""
    auth_key = {'key': '123'}  # Задаем неверный ключ api и сохраняем в переменную auth_key
    status, result = pf.get_list_of_pets(auth_key, filter)  # Запрашиваем список питомцев
    assert status == 403  # Сверяем полученный ответ с ожидаемым результатом


def test_create_pet_simple_with_valid_data(name='Вася', animal_type='кот', age='3'):
    """Проверяем, что можно упрощенно добавить питомца с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200  # Сверяем полученный ответ с ожидаемым результатом
    assert result['name'] == name  # Сверяем полученный ответ с ожидаемым результатом


def test_create_pet_simple_with_invalid_key(name='Вася', animal_type='кот', age='3'):
    """Проверяем, что запрос на упрощенное добавление питомца с неверным api ключом возвращает код 403"""
    auth_key = {'key': '123'}  # Задаем неверный ключ api и сохраняем в переменную auth_key
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)  # Создаем питомца
    assert status == 403  # Сверяем полученный ответ с ожидаемым результатом


def test_add_new_pet_with_invalid_data(name='Барбоскин', animal_type='cat',
                                       age='4', pet_photo='images/catt.txt'):
    """Проверяем что можно добавить питомца с некорректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)  # Получаем путь изображения питомца и сохраняем в pet_photo
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # Запрашиваем ключ api и сохраняем в переменную auth_key

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)  # Добавляем питомца

    assert status == 400  # Сверяем полученный ответ с ожидаемым результатом
    # Тут баг, так как в качестве фото принимает txt файл


def test_successful_set_photo():
    """Проверяем возможность установки фото питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)  # Получаем ключ auth_key
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")  # Запрашиваем список своих питомцев
    pet_photo = os.path.join(os.path.dirname(__file__), 'images/dog.jpg')  # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    if len(my_pets['pets']) > 0:
        status, result = pf.set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200  # Сверяем полученный ответ с ожидаемым результатом
    else:
        raise Exception("There is no my pets")


def test_create_pet_simple_with_invalid_data(name='Вася', animal_type=int(2), age='3'):
    """Проверяем, что запрос на упрощенное добавление питомца с неверным api ключом возвращает код 403"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)  # Создаем питомца
    assert status == 400  # Сверяем полученный ответ с ожидаемым результатом
    # Тут баг, так как в качестве типа животного принимает числа


def test_create_pet_simple_with_invalid_data2(name=int(32), animal_type='кот', age='3'):
    """Проверяем, что запрос на упрощенное добавление питомца с неверным api ключом возвращает код 403"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)  # Создаем питомца
    assert status == 400  # Сверяем полученный ответ с ожидаемым результатом
    # Тут баг, так как в качестве имени животного принимает числа


def test_unsuccessful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце с неверным api ключом"""

    auth_key = {'key': '123'}  # Задаем неверный ключ api и сохраняем в переменную auth_key
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 403
    else:
        # если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
    # Тут баг, так как при неверном api ключе не выдает код 403
