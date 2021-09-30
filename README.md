## 스파르타내일배움캠프 첫 번째 프로젝트(Weling)
![Generic badge](https://img.shields.io/badge/pycharm-3.8-{yellowgreen}.svg) ![Generic badge](https://img.shields.io/badge/Robo 3T-1.4.4-{green}.svg) ![Generic badge](https://img.shields.io/badge/mongoDB-5.0-{orange}.svg) ![Generic badge](https://img.shields.io/badge/Flask-2.0.1-{blue}.svg)  

![]
(https://github.com/jtheeeeee/we_are_traveling/blob/main/static/img/logo.png) 


### 🔗라이브
[We-ling.shop.kr](We-ling.shop.kr)  

### ✈️ 소개
위링(we-ling)은 여행을 기반으로한 정보 공유 및 커뮤니티 기능을 가지고 있습니다.
We are traveling의 약자이며 여행자들을 대상으로 서비스를 제공합니다.  

### 🛠 기능 요약
1. 웹사이트 이용자가 여행 전, 여행 계획 및 예산안을 작성, 공유하고 이용자들의 의견을 얻을 수 있도록 정보 공유를 목적으로 하는 커뮤니티 기능을 가집니다.
2. 웹사이트 이용자가 여행 후, 여행 날짜/여행 사진/제목/여행 주소/여행 내용(예산안, 이동 경로)를 작성하고 이를 열람함으로써 여행 일지를 공유할 수 있습니다.  

### ⏰ 개발 기간
2021년 9월 23일 ~ 2021년 09월 30일  

### 👩‍💻 멤버 구성
- 정태희(팀장)
- 김혜린
- 서성혁
- 우성호  

### 📌 기술
- HTML, CSS, JavaScript, Ajax, Jinja, jQuery
- pycharm, Robo3-T
- Flask, jinja2, aws, mongodb  

### 📌 기술 선택 이유
- Flask: Flask는 다양한 웹 엔진과 붙여서 사용할 수 있으며 코드가 다른 프레임워크인 Django에 비해 비교적 단순하기 때문에 선택하였고. 또한, API서버를 만드는데 매우 편리하기 때문에 백엔드를 중심으로 개발하는 이번 프로젝트에 적합하다고 판단하였습니다.

- jinja2: Flask 사용시 html코드 내에서 파이썬 API에서 보내는 정보의 출력이나, html코드의 동적 제어등을 쉽게 사용할 수 있기 때문입니다.

- aws: 팀 프로젝트로 완성한 서비스를 서버로 제공할 때 Amazon EC2의 웹 서비스 인터페이스를 사용하여 인스턴스(서버)를 쉽고 간단하게 구현할 수 있으며, 높은 안정성으로 유연하게 서비스 관리를 할 수 있기 때문에 aws를 선택하였습니다. 

- mongoDB: RDBMS보다 빠른 속도를 가지고 있기 때문에 데이터를 읽고 쓰기가 빠르며, JSON과 같은 동적 스키마형 도큐먼트들을 선호함에 따라 특정한 종류의 애플리케이션을 더 쉽고 더 빠르게 데이터 통합을 가능하게 하기 때문에 선택하였습니다. 데이터 복제를통해 가용성을 향상시킬수 있습니다.

- kakao 우편번호 서비스(API): API 정보를 쉽게 사용할수 있고, API TOKEN 없이도 사용할 수 있는 정보들이 많아서 편리합니다.

### 📌 주요 기능
- 게시글 작성: 한 장의 사진과 함께 여행 경험을 작성할 수 있습니다.

- 게시글 수정: 게시글의 날짜, 사진, 주소, 내용을 수정할수 있는화면을 제공합니다.

- 게시글 삭제: 게시글이 마음에 안들경우 삭제 버튼을 눌러 지울수 있습니다.

- 게시글 리스트 조회: 게시글의 대표사진을 카드 형식으로 리스트를 제공합니다.

- kakao 우편번호 API: 여행 장소의 구체적인 주소를 검색할 수 있는 기능을 제공합니다.  

### 📌 문제 해결!
