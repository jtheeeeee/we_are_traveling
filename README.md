스파르타내일배움캠프 첫 번째 프로젝트 (Weling)

라이브
-도메인 ex): We-ling.shop .kr .

소개
위링(we-ling)은 여행을 기반으로한 정보 공유 및 커뮤니티 기능을 가지고 있습니다. 
We are traveling의 약자이며 여행자들을 대상으로 서비스를 제공합니다. 

기능 요약
1)웹사이트 이용자가 여행 전, 여행 계획 및 예산안을 작성, 공유하고 이용자들의 의견을 얻을 수 있도록 정보 공유를 목적으로 하는 커뮤니티 기능을 가집니다.

2)웹사이트 이용자가 여행 후, 여행 날짜/여행 사진/제목/여행 주소/여행 내용(예산안, 이동 경로)를 작성하고 이를 열람함으로써 여행 일지를 공유할 수 있습니다.

개발기간
2021년 9월 23일 ~ 2021년 09월 30일 

멤버구성
김혜린, 서성혁, 우성호, 정태희(대장)

기술
- HTML, CSS, JavaScript, Ajax, Jinja, jQuery
- pycharm, Robo3-T
- Flask, jinja2, aws, mongodb 
---------------------------
기술 선택 이유(wiki)
- Flask: Flask는 다양한 웹 엔진과 붙여서 사용할 수 있으며 코드가 다른 프레임워크인 Django에 비해 비교적 단순하기 때문에 선택하였고. 또한, API서버를 만드는데 매우 편리하기 때문에 백엔드를 중심으로 개발하는 이번 프로젝트에 적합하다고 판단하였습니다.

- jinja2: Flask 사용시 html코드 내에서 파이썬 API에서 보내는 정보의 출력이나, html코드의 동적 제어등을 쉽게 사용할 수 있기 때문입니다.

- aws: 팀 프로젝트로 완성한 서비스를 서버로 제공할 때 Amazon EC2의 웹 서비스 인터페이스를 사용하여 인스턴스(서버)를 쉽고 간단하게 구현할 수 있으며, 높은 안정성으로 유연하게 서비스 관리를 할 수 있기 때문에 aws를 선택하였습니다. 

- mongoDB: RDBMS보다 빠른 속도를 가지고 있기 때문에 데이터를 읽고 쓰기가 빠르며, JSON과 같은 동적 스키마형 도큐먼트들을 선호함에 따라 특정한 종류의 애플리케이션을 더 쉽고 더 빠르게 데이터 통합을 가능하게 하기 때문에 선택하였습니다. 데이터 복제를통해 가용성을 향상시킬수 있습니다.

- kakao 우편번호 서비스(API): API 정보를 쉽게 사용할수 있고, API TOKEN 없이도 사용할 수 있는 정보들이 많아서 편리합니다.

-------------
주요 기능(wiki)

- 게시글 작성: 한 장의 사진과 함께 여행 경험을 작성할 수 있습니다.

- 게시글 수정: 게시글의 날짜, 사진, 주소, 내용을 수정할수 있는화면을 제공합니다.

- 게시글 삭제: 게시글이 마음에 안들경우 삭제 버튼을 눌러 지울수 있습니다.

- 게시글 리스트 조회: 게시글의 대표사진을 카드 형식으로 리스트를 제공합니다.

- kakao 우편번호 API: 여행 장소의 구체적인 주소를 검색할 수 있는 기능을 제공합니다. 

--------------
트러블 슈팅 
Weling 문제 해결


정태희
1. 이미지 저장 문제
- 게시물 업로드시 이미지를 업로드하지 않는 경우와 게시물 수정시 이미지를 업로드하지 않는 경우에 이미지 태그의 파일값을 불러오는 부분이 undefined로 처리되어 API가 호출되지 않는 에러가 발생.

- 1차 시도: file type의 input 태그에 default 이미지를 넣는 방법을 찾아보았으나 보안 상의 이유로 불가능하다는 답변을 발견.

- 해결: 이미지 파일의 유무를 확인하는 변수(bool)을 선언하여 파일의 부재시 임의로 data를 넣어 API를 호출하는 방향으로 해결. API로 넘어온 변수(bool)에 따라 분기문으로 나누어 데이터 업로드 및 업데이트.

@app.route('/api/insert_form', methods=['POST'])
def save_insert() :
    datas = list(db.weling.find({}))
    id = int(datas[-1]['id']) + 1
    bool = request.form['bool'] # file값의 유무를 확인 하는 변수
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

   if bool == 'True' :                 #file값이 존재하는 경우 기존에 썼던 코드와 같이 file을 새로 저장
        file = request.files['file_give']
        extention = file.filename.split('.')[-1]
        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'file-{mytime}'
        save_to = f'static/{filename}.{extention}'
        file.save(save_to)
        doc.update({'file' : f'{filename}.{extention}'})
    elif bool == 'False' :              #file값이 존재하지 않는 경우에 default파일을 저장
        filename = "sparta.png"
        doc.update({'file' : filename})
    db.weling.insert_one(doc)
    return jsonify({'result' : 'success', 'msg' : '작성 완료'})


김혜린
1. 게시글 저장하고 DB로 넘기는 API 기능 구현 중 Jquery 문법에 #이 없었다

우성호
1. Pagination 기능 구현중 JavaScript 사용시 문제가 발생하여 Jinja 문법을 사용하여 수정 하였다.
    <div class="page">
{% if block_start - 1 > 0 %}
    <a  // href="{{url_for('board_list', page=block_start - 1)}}" >[이전]</a>
{% endif %}
{% for i in range(block_start, block_end + 1)%}
    {% if i > last_page_num %}
    {% else %}
        {% if i == page %}
            <b>{{ i }}</b>
        {% else %}
            <a  // href="{{url_for('board_list', page=i)}}">{{ i }}</a>
        {% endif %}
    {% endif %}
{% endfor %}
{% if block_end < last_page_num %}
    <a  // href="{{url_for('board_list', page=block_end + 1)}}"  >[다음]</a>
{% endif %}
    </div>

2. 몽고DB에서 데이터를 조회하는 과정에서 Ajax로 코드를 구현하였지만 문제가 발생하여 Jinja문법을 사용해서 해결 하였다.
                   {% for data in datas %}
                    <li>
                        <figure class="snip">
                            <a href="javascript:void(0);" onclick="update();">
                                <figcaption>
                                    <p>{{data.title}}</p>
                                </figcaption>
                                <a // href = '/api/detail/{{ data.id}}' >
                                 <img // src= /static/{{data.file}}
                                     // alt="여행장소"/></a>
                            </a>
                        </figure>
                    </li>
                    {% endfor %}

서성혁-
1. 주소 입력 후 주소 API창이 닫히지않음 확인. Function형식이 맞지않아 Kakao API site에서 정보를 다시 받아와 입력후 해결.

               
   function postcode() {
          new daum.Postcode({
              oncomplete: function (data) {
             var addr = ''; 
             if (data.userSelectedType === 'R') { 
                            addr = data.roadAddress;
                        } else { 
                            addr = data.jibunAddress;
                        }
                        document.getElementById('postcode').value = data.zonecode;
                        document.getElementById("roadAddress").value = addr;              
                        document.getElementById("detailAddress").focus();
                    }
                }).open();
            }
 
