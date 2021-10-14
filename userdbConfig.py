from pymongo import MongoClient
import hashlib

client = MongoClient('localhost', 27017)
db = client.dbweling


for i in range(10):
    username_receive = 'id'+str(i)
    password_receive = 'pwpw'+str(i)
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()

    doc = {
        "username" : username_receive,  # 아이디
        "password" : password_hash,  # 비밀번호
        "profile_name" : username_receive,  # 프로필 이름 기본값은 아이디
        "profile_pic_real" : "profile_placeholder.png",  # 프로필 사진 기본 이미지
    }
    db.users.insert_one(doc)