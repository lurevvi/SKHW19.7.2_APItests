import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """АПИ библиотека к веб приложению PetFriends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email, password) -> json:
        """Метод запроса для получения АПИ ключа"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter) -> json:
        """Метод запроса, возвращающий список найденных питомцев, совпадающих с фильтром"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Метод отправляет на сервер данные о новом добавляемом питомце"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер об обновлении данных питомца по указанному ID"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status,

    def create_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет на сервер данные о новом добавляемом питомце без фото"""

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
            }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def set_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет запрос на сервер об обновлении фотографии питомца по указанному ID"""

        data = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
