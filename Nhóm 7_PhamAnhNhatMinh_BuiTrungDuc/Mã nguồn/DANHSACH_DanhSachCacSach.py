import json
import os

import DOITUONG_Sach

DsSachObject = []
fileSachJson = "data/books.json"
fileUserJson = "data/users.json"
API_URL = "https://openlibrary.org/search.json"

def docFileJson():
    if os.path.exists(fileSachJson):
        with open (fileSachJson, 'r', encoding='utf-8') as file:
            sach_dict = json.load(file)
            return [DOITUONG_Sach.Sach.from_dict(sach) for sach in sach_dict]
    return []

def luuVaoFileJson():
    with open (fileSachJson, 'w', encoding='utf-8') as file:
        json.dump([sach.toDict() for sach in DsSachObject], file, ensure_ascii=False, indent=4)

def capNhatLaiDanhSach(lst):
    global DsSachObject
    DsSachObject = lst

def capNhatSach(idSach, tenMoi, tacGiaMoi, namXBMoi, duongDanMoi):
    for sach in DsSachObject:
        if sach.id == idSach:
            sach.ten = tenMoi
            sach.tacGia = tacGiaMoi
            sach.namXB = namXBMoi
            sach.duongDan = duongDanMoi
            break
    luuVaoFileJson()

def docFileUserJson():
    if os.path.exists(fileUserJson):
        with open(fileUserJson, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def luuUserVaoFileJson(users):
    with open(fileUserJson, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

def themUser(username, password, role="user"):
    users = docFileUserJson()
    if any(user["username"] == username for user in users):
        return False  # Tránh trùng lặp
    users.append({"username": username, "password": password, "role": role})
    luuUserVaoFileJson(users)
    return True

def xacThucUser(username, password):
    users = docFileUserJson()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user["role"]  # Trả về quyền nếu hợp lệ
    return None  # Không tìm thấy

 