from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import math

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'WELING'

client = MongoClient('localhost', 27017)
db = client.dbweling


@app.route("/")
def board_list():
    # board = mongo.db.board
    # board = db
    # 페이지 값 (디폴트값 = 1)
    page = request.args.get("page", 1, type=int)
    # 한 페이지 당 몇 개의 게시물을 출력할 것인가
    limit = 8

    # datas = db.weling.find({}).skip((page - 1) * limit).limit(limit)  # board컬럭션에 있는 모든 데이터를 가져옴
    datas = list(db.weling.find({}).skip((page - 1) * limit).limit(limit)) # board컬럭션에 있는 모든 데이터를 가져옴


    # same_ages = list(db.weling.find({}, {'_id': False}))
    # user = db.users.find_one({'name': 'bobby'})

    # print(datas)

    # 게시물의 총 개수 세기
    # tot_count = board.find({}).count()
    tot_count = db.weling.count()
    # print(tot_count)


    # 마지막 페이지의 수 구하기
    last_page_num = math.ceil(tot_count / limit) # 반드시 올림을 해줘야함
    # print(last_page_num)

    #
    # 페이지 블럭을 5개씩 표기
    block_size = 5
    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_num = int((page - 1) / block_size)
    # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_start = (block_size * block_num) + 1
    # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    block_end = block_start + (block_size - 1)

    # print(datas)
    # print(limit)
    # print(page)
    # print(block_start)
    # print(block_end)
    # print(last_page_num)

    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        print(user_info)
        return render_template("main.html", datas=datas, limit=limit, page=page, block_start=block_start,
                               block_end=block_end, last_page_num=last_page_num, user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("main", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("main", msg="로그인 정보가 존재하지 않습니다."))


# 메인화면 이동
@app.route('/main')
def main():
    # board = mongo.db.board
    # board = db
    # 페이지 값 (디폴트값 = 1)
    page = request.args.get("page", 1, type=int)
    # 한 페이지 당 몇 개의 게시물을 출력할 것인가
    limit = 8

    # datas = db.weling.find({}).skip((page - 1) * limit).limit(limit)  # board컬럭션에 있는 모든 데이터를 가져옴
    datas = list(db.weling.find({}).skip((page - 1) * limit).limit(limit)) # board컬럭션에 있는 모든 데이터를 가져옴


    # same_ages = list(db.weling.find({}, {'_id': False}))
    # user = db.users.find_one({'name': 'bobby'})

    # print(datas)

    # 게시물의 총 개수 세기
    # tot_count = board.find({}).count()
    tot_count = db.weling.count()
    # print(tot_count)


    # 마지막 페이지의 수 구하기
    last_page_num = math.ceil(tot_count / limit) # 반드시 올림을 해줘야함
    # print(last_page_num)

    #
    # 페이지 블럭을 5개씩 표기
    block_size = 5
    # 현재 블럭의 위치 (첫 번째 블럭이라면, block_num = 0)
    block_num = int((page - 1) / block_size)
    # 현재 블럭의 맨 처음 페이지 넘버 (첫 번째 블럭이라면, block_start = 1, 두 번째 블럭이라면, block_start = 6)
    block_start = (block_size * block_num) + 1
    # 현재 블럭의 맨 끝 페이지 넘버 (첫 번째 블럭이라면, block_end = 5)
    block_end = block_start + (block_size - 1)

    # print(datas)
    # print(limit)
    # print(page)
    # print(block_start)
    # print(block_end)
    # print(last_page_num)


    msg = request.args.get("msg")
    return render_template('main.html', msg=msg,datas=datas, limit=limit, page=page, block_start=block_start,
                               block_end=block_end, last_page_num=last_page_num)

# 회원가입후 로그인창으로 이동
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)



# 로그인 서버
@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

# 회원가입 서버
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    bool = request.form['bool']
    username = request.form['username_give']
    password = request.form['password_give']
    usernickname = request.form['nickname_give']
    userdata = request.form['userdata_give']
    usergender = request.form['usergender_give']

    print(username, password, usernickname, userdata, usergender)

    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    doc = {
        'username': username,  # 아이디
        'password': password_hash,  # 비밀번호
        'usernickname': usernickname,  # 프로필 닉네임
        'userdata': userdata,  # 생년월일
        'usergender': usergender  # 성별
    }

    if bool == 'True':
        userfile = request.files['userfile_give']
        extention = userfile.filename.split('.')[-1]
        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'userfile-{mytime}'
        save_to = f'static/userfile/{filename}.{extention}'
        userfile.save(save_to)
        doc.update({'userfile': f'{filename}.{extention}'})
    elif bool == 'False':
        filename = "profile_placeholder.png"
        doc.update({'userfile': filename})

    db.users.insert_one(doc)
    return jsonify({'result': 'success'})



# 아이디 중복확인 서버
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})












@app.route('/insert')
def insert():
    return render_template('insert_form.html')

@app.route('/api/insert_form', methods=['POST'])
def save_insert() :
    datas = list(db.weling.find({}))
    id = int(datas[-1]['id']) + 1
    bool = request.form['bool']
    date = request.form['date_give']
    title = request.form['title_give']
    roadaddress = request.form['roadaddress_give']
    detailaddress = request.form['detailaddress_give']
    postcode = request.form['postcode_give']
    content = request.form['content_give']
    doc = {
        'id' : id,
        'date' : date,
        'title' : title,
        'postcode' : postcode,
        'roadaddress' : roadaddress,
        'detailaddress' : detailaddress,
        'content' : content
    }

    if bool == 'True' :
        file = request.files['file_give']
        extention = file.filename.split('.')[-1]
        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'file-{mytime}'
        save_to = f'static/{filename}.{extention}'
        file.save(save_to)
        doc.update({'file' : f'{filename}.{extention}'})
    elif bool == 'False' :
        filename = "sparta.png"
        doc.update({'file' : filename})

    db.weling.insert_one(doc)
    return jsonify({'result' : 'success', 'msg' : '작성 완료'})


@app.route("/api/detail/<int:id>", methods=['GET'])
def read(id) :
    datas=list(db.weling.find({}))
    end=len(datas)
    print(id)
    print(list(db.weling.find({'id':id})))
    data= list(db.weling.find({'id':id}))[0]
    index=datas.index(data)
    next_index = index +1
    prev_index = index -1
    if next_index > end-1 :
        next_index = 0
    next_data_id= datas[next_index]['id']
    prev_data_id=datas[prev_index]['id']
    return render_template("detail.html", data=data, next_id=next_data_id, prev_id=prev_data_id)

@app.route("/api/update/<int:id>", methods=['GET'])
def update(id):
    data = list(db.weling.find({'id' : id}))[0]
    return render_template("update.html",data=data)



@app.route("/api/update-upload", methods=['POST'])
def update_upload() :
    bool = request.form['bool']
    file_name = request.form['file_name']
    print(file_name)
    date = request.form['date_give']
    title = request.form['title_give']
    roadaddress = request.form['roadaddress_give']
    detailaddress = request.form['detailaddress_give']
    postcode = request.form['postcode_give']
    content = request.form['content_give']
    doc = {
        'date' : date,
        'title' : title,
        'postcode' : postcode,
        'roadaddress' : roadaddress,
        'detailaddress' : detailaddress,
        'content' : content
    }
    print(doc)
    if bool == 'True' :
        file = request.files['file_give']
        if file_name == 'sparta.png' :
            extention = file.filename.split('.')[-1]
            today = datetime.now()
            mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
            filename = f'file-{mytime}'
            save_to = f'static/{filename}.{extention}'
            file.save(save_to)
            doc.update({'file' : f'{filename}.{extention}'})
        else :
            save_to = f'static/{file_name}'
            file.save(save_to)
            doc.update({'file' : f'{file_name}'})

    print(type(request.form['id']))
    db.weling.update_one({'id' : int(request.form['id'])}, {'$set' : doc})
    return jsonify({'result' : 'success', 'msg' : '수정 완료'})


@app.route('/api/delete', methods=['DELETE'])
def delete():
    id_receive = request.form['id_give']
    print(id_receive)
    db.weling.delete_one({'id' : int(id_receive)})
    return jsonify({'result': 'success', 'msg': '삭제 완료'})
    # return render_template("main.html")


@app.route('/api/comment-save', methods=['POST'])
def comment_save():
    comment_receive = request.form['comment_give']
    date_receive = request.form['date_give']
    print(comment_receive)
    return jsonify({'result' : 'success', 'msg' : comment_receive+date_receive})


if __name__ == '__main__' :
    app.run('0.0.0.0', port=5000, debug=True)
