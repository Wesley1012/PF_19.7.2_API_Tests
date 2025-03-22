from api import PetFriends
from settings import valid_password, valid_login, invalid_login, invalid_password
import os

pf = PetFriends()
_, auth_key = pf.get_api_key(valid_login, valid_password)
invalid_auth_key = {"key" :"a12642ed39615a40fa3f025babbcea6aac64f9670a556febc0647c3a"}


# Получение auth ключа с невалидными данными
def test_get_api_key_with_invalid_user(email=invalid_login, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result

# Получение auth ключа с пустым логином
def test_get_api_with_empty_email(email="", password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result

# Получение auth ключа с пустым паролем
def test_get_api_with_empty_password(email=valid_login, password=""):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result

# Получение списка питомцев с невалидным ключем
def test_get_list_of_pets_with_invalid_auth_key(filter=""):
    status, result = pf.get_list_pets(invalid_auth_key, filter)
    assert status == 403
    assert "pets" not in result

# Удаление питомца с невалидным ключем
def test_delete_pet_with_invalid_auth_key():
    _, pets_list_before_delete = pf.get_list_pets(auth_key, "my_pets")
    pet_id = pets_list_before_delete["pets"][0]["id"]
    status, result = pf.delete_pet(invalid_auth_key, pet_id)
    _, pets_list_after_delete = pf.get_list_pets(auth_key, "my_pets")
    assert status == 403
    assert pet_id == pets_list_after_delete["pets"][0]["id"]

# Добавление нового питомца с невалидным ключем
def test_add_pet_with_invalid_auth_key(name="Яростный", animal_type="Шамиль", age=50):
    status, result = pf.add_new_pet_without_photo(invalid_auth_key, name, animal_type, age)
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    assert status == 403
    assert name not in my_pets["pets"]

# Добавление информации о питомце с невалидным ключем
def test_update_pet_info_with_invalid_auth_key(name="Джанго", animal_type="Освобожденный", age=228):
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    if len(my_pets["pets"]) == 0:
        _, new_pet = pf.add_new_pet_without_photo(auth_key, name="", animal_type="", age=0)
        _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    pet_id = my_pets["pets"][0]["id"]
    status, result = pf.update_pet_info(invalid_auth_key, pet_id, name, animal_type, age)
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    assert status == 403
    assert name not in my_pets["pets"]

# Добавление фото питомцу с невалидным ключем
def test_add_photo_for_pet_with_invalid_auth_key():
    pet_photo = os.path.join(os.path.dirname(__file__), "images/Dog.jpg")
    _, new_pet = pf.add_new_pet_without_photo(auth_key, name="PhotoTest", animal_type="Animal", age=2077)
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    pet_id = my_pets["pets"][0]["id"]
    status, _ = pf.add_photo_for_pet(invalid_auth_key, pet_id, pet_photo)
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    assert status == 403
    assert not my_pets["pets"][0]["pet_photo"]
    # Удаляем питомца(Опционально)
    pf.delete_pet(auth_key, pet_id)

# Добавление информации чужому питомцу
def test_update_another_pet_info(name="ПочемуБы", animal_type="ИНет", age=1312):
    _, all_pets = pf.get_list_all_pets(auth_key, "all_pets")
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    # Проверка того что питомец чужой
    my_pets_ids = [i["id"] for i in my_pets["pets"]]
    if len(all_pets["pets"]) > 0:
        for pet in all_pets["pets"]:
            if pet["id"] in my_pets_ids:
                continue
            else:
                status, _ = pf.update_pet_info(auth_key, pet["id"], name, animal_type, age)
                break
                _, all_pets = pf.get_list_all_pets(auth_key, "all_pets")
                assert status == 403
                assert name not in all_pets["pets"]
    else:
        raise Exception("Nothing to change!")

# Добавление фото чужому питомцу
def test_add_pet_with_photo_through_create_pet_simple():
    pet_photo = os.path.join(os.path.dirname(__file__), "images/Dog.jpg")
    _, all_pets = pf.get_list_all_pets(auth_key, "all_pets")
    _, my_pets = pf.get_list_pets(auth_key, "my_pets")
    # Проверка того что питомец чужой
    my_pets_ids = [i["id"] for i in my_pets["pets"]]
    if len(all_pets["pets"]) > 0:
        for pet in all_pets["pets"]:
            if pet["id"] in my_pets_ids:
                continue
            else:
                status, _ = pf.add_photo_for_pet(auth_key, pet["id"], pet_photo)
                break
                _, all_pets = pf.get_list_all_pets(auth_key, "all_pets")
                assert status == 403
                assert pet_photo not in all_pets["pets"]
    else:
        raise Exception("Nothing to chenge!")

