from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import pyodbc
import base64
from django.core.files.base import ContentFile
    
@csrf_exempt
def calendar(request):
    if request.method == 'POST':
        # POST 요청의 경우 처리 로직을 구현합니다.
        try:
            data = json.loads(request.body)
            id_key = data['id_key']

            # 데이터 베이스 연동
            db = pyodbc.connect(DSN='Tibero6', uid='HE0O0NJE', pwd='1234')
            curs = db.cursor()

            # 사용자의 일정 정보를 DB에서 받아옴
            sql = "SELECT START_DAY, END_DAY FROM Schedule WHERE USER_ID = ?"
            curs.execute(sql, id_key)

            # 사용자의 일정 정보
            response_data = []

            # 일정 정보 가져오기
            rows = curs.fetchall()
            for row in rows:
                start_date = row[0]  # 시작 날짜
                end_date = row[1]  # 종료 날짜
            
                # 일정 정보를 딕셔너리 형태로 저장
                schedule = {
                    'start_date': start_date,
                    'end_date': end_date
                }

                # 일정 정보를 리스트에 추가
                response_data.append(schedule)

            # 연결 종료
            curs.close()
            db.close()
            
            return JsonResponse(response_data, safe=False)
        except json.JSONDecodeError as e:
            response_data = {
                'message': '잘못된 요청입니다. JSON 형식이 올바르지 않습니다.',
            }
            return JsonResponse(response_data, status=400)
    else:
        # POST 요청이 아닌 경우 예외 처리를 수행하거나 다른 로직을 구현할 수 있습니다.
        response_data = {
            'message': '잘못된 요청입니다.'
        }
        return JsonResponse(response_data, status=400)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data['id']
            password = data['password']

            # 데이터 베이스 연동            
            # 아이디와 비밀번호 일치 여부 확인
            db = pyodbc.connect(DSN='Tibero6', uid='HE0O0NJE', pwd='1234')
            curs = db.cursor()
            
            sql = "SELECT id FROM Users WHERE user_id = ? AND password = ?"
            curs.execute(sql, (user_id, password))
            row = curs.fetchone()
            if row:
                # 로그인 성공 처리 및 추가 작업 수행
                id_key = row[0]
                success_login=True
            else:
                # 로그인 실패 처리
                success_login=False

            curs.close()
            db.close()

            response_data = {
                'login_result': success_login,
                'id_key': id_key,
            }
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            response_data = {
                'message': '잘못된 요청입니다. JSON 형식이 올바르지 않습니다.',
            }
            return JsonResponse(response_data, status=400)
    else:
        response_data = {
            'message': '잘못된 요청입니다.'
        }
        return JsonResponse(response_data, status=400)
    
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        # POST 요청의 경우 처리 로직을 구현합니다.
        try:
            data = json.loads(request.body)
            id = data['id']
            password = data['password']
            name = data['name']
            birthDate = data['birthDate']
            email = data['email']
            
            # 데이터 베이스 연동
            db = pyodbc.connect(DSN='Tibero6', uid='HE0O0NJE', pwd='1234')
            curs = db.cursor()

            # 데이터 입력
            sql = "INSERT INTO Users (id, user_id, password, user_name, date_of_birth, email) VALUES (SEQ_ID.NEXTVAL, ?, ?, ?, ?, ?)"
            curs.execute(sql, (id, password, name, birthDate, email))
            db.commit()  # 변경 사항 커밋

            sql = "SELECT id FROM Users WHERE user_id = ? AND password = ?"
            curs.execute(sql, (id, password))
            row = curs.fetchone()
            if row:
                # 로그인 성공 처리 및 추가 작업 수행
                id_key = row[0]

            curs.close()
            db.close()

            successSignup=True; #회원가입 성공 시 true, 실패 시 false 가 되는 로직을 수행
            # 응답 데이터를 만들어 클라이언트에게 전송합니다.
            response_data = {
                'successSignup' : successSignup,
                'id_key':id_key,
                'message': '회원가입 성공!',
            }
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            response_data = {
                'message': '잘못된 요청입니다. JSON 형식이 올바르지 않습니다.',
            }
            return JsonResponse(response_data, status=400)
    else:
        # POST 요청이 아닌 경우 예외 처리를 수행하거나 다른 로직을 구현할 수 있습니다.
        response_data = {
            'message': '잘못된 요청입니다.'
        }
        return JsonResponse(response_data, status=400)

@csrf_exempt
def schedule(request):
    if request.method == 'POST':
        # POST 요청의 경우 처리 로직을 구현합니다.
        try:
            data = json.loads(request.body)
            id_key = data['id_key']
            selectedDate = data['selectedDate']
            
            # 데이터 베이스 연동
            db = pyodbc.connect(DSN='Tibero6', uid='HE0O0NJE', pwd='1234')
            curs = db.cursor()

            # 데이터 조회
            # 데이터베이스에서 id_key와 선택 날짜를 통해 일정 데이터를 불러온다.
            query = "SELECT TITLE FROM SCHEDULE WHERE USER_ID = ? AND ? BETWEEN START_DAY AND END_DAY"
            curs.execute(query, id_key, selectedDate)
            schedule_rows = curs.fetchall()

            curs.close()
            db.close()

            schedule_data = []
            for row in schedule_rows:
                # 각 row에서 필요한 정보를 추출하여 schedule_data에 추가합니다.
                schedule_data.append({
                    'title': row[0],
                    # 추가적인 필드 정보를 추출하여 딕셔너리 형태로 저장합니다.
                })
            
            # 응답 데이터를 만들어 클라이언트에게 전송합니다.
            response_data = {
                'schedule': schedule_data,
                'message': '일정 불러오기 성공!',
            }
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            response_data = {
                'message': '잘못된 요청입니다. JSON 형식이 올바르지 않습니다.',
            }
            return JsonResponse(response_data, status=400)
    else:
        # POST 요청이 아닌 경우 예외 처리를 수행하거나 다른 로직을 구현할 수 있습니다.
        response_data = {
            'message': '잘못된 요청입니다.'
        }
        return JsonResponse(response_data, status=400)
    
@csrf_exempt
def addpost(request):
    if request.method == 'POST':
        # POST 요청의 경우 처리 로직을 구현합니다.
        try:
            data = json.loads(request.body)
            id_key = data['id_key']
            title = data['title']
            startDay = data['startDay']
            endDay= data['endDay']
            
            # 데이터 베이스 연동
            db = pyodbc.connect(DSN='Tibero6', uid='HE0O0NJE', pwd='1234')
            curs = db.cursor()

            # 데이터 입력
            sql = "INSERT INTO Schedule (TITLE, START_DAY, END_DAY, POST_IMG, USER_ID) VALUES (?, ?, ?, NULL, ?)"
            curs.execute(sql, (title, startDay, endDay, id_key))
            db.commit()  # 변경 사항 커밋

            curs.close()
            db.close()
            response_data = {
                'message': '일정추가 성공!.'
                }
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            response_data = {
                'message': '잘못된 요청입니다. JSON 형식이 올바르지 않습니다.',
            }
            return JsonResponse(response_data, status=400)
    else:
        # POST 요청이 아닌 경우 예외 처리를 수행하거나 다른 로직을 구현할 수 있습니다.
        response_data = {
            'message': '잘못된 요청입니다.'
        }
        return JsonResponse(response_data, status=400)
    
@csrf_exempt
def profile(request):
    if request.method == 'POST':
        # POST 요청의 경우 처리 로직을 구현합니다.
        try:
            data = json.loads(request.body)
            id_key = data['id_key']
            
            # 데이터 베이스 연동
            db = pyodbc.connect(DSN='Tibero6', uid='HE0O0NJE', pwd='1234')
            curs = db.cursor()

            # 데이터 조회
            # 데이터베이스에서 사용자의 아이디와 이메일, 생년월일을 불러온다.
            query = "SELECT USER_ID, USER_NAME, DATE_OF_BIRTH, EMAIL FROM USERS WHERE ID=?"
            curs.execute(query, id_key)
            
            rows = curs.fetchall()
            for row in rows:
                user_id = row[0]
                user_name = row[1]
                date_of_birth = row[2]
                email = row[3]

            curs.close()
            db.close()
            
            # 응답 데이터를 만들어 클라이언트에게 전송합니다.
            response_data = {
                'user_id': user_id,
                'user_name': user_name,
                'date_of_birth': date_of_birth,
                'email': email,
                'message': '일정 불러오기 성공!',
            }
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            response_data = {
                'message': '잘못된 요청입니다. JSON 형식이 올바르지 않습니다.',
            }
            return JsonResponse(response_data, status=400)
    else:
        # POST 요청이 아닌 경우 예외 처리를 수행하거나 다른 로직을 구현할 수 있습니다.
        response_data = {
            'message': '잘못된 요청입니다.'
        }
        return JsonResponse(response_data, status=400)

@csrf_exempt
def photo(request):
    if request.method == 'POST':
        # POST 요청의 경우 처리 로직을 구현합니다.
        try:
            data = json.loads(request.body)
            id_key = data['id_key']
            base64_image = data['image']
            format, imgstr = base64_image.split(';base64,')  # format과 imgstr를 분리
            image = base64.b64decode(imgstr)  # imgstr을 바이너리로 바꾸기

            
            # 데이터 베이스 연동
            db = pyodbc.connect(DSN='Tibero6', uid='HE0O0NJE', pwd='1234')
            curs = db.cursor()




            ## 여기서 모델로부터 title과 start_day, end_day 를 받아옴
            ## ----------------------------------------------------
            title="2023 네이버웹툰 지상 최대 공모전"
            startDay="2023-06-23"
            endDay="2023-06-25"



            # 데이터 입력
            sql = "INSERT INTO Schedule (TITLE, START_DAY, END_DAY, POST_IMG, USER_ID) VALUES (?, ?, ?, ?, ?)"
            curs.execute(sql, (title, startDay, endDay, image, id_key))
            db.commit()  # 변경 사항 커밋

            curs.close()
            db.close()
            response_data = {
                'title': title,
                'startDay': startDay,
                'endDay': endDay,
                'image': image,
                'message': '일정추가 성공!.'
                }
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            response_data = {
                'message': '잘못된 요청입니다. JSON 형식이 올바르지 않습니다.',
            }
            return JsonResponse(response_data, status=400)
    else:
        # POST 요청이 아닌 경우 예외 처리를 수행하거나 다른 로직을 구현할 수 있습니다.
        response_data = {
            'message': '잘못된 요청입니다.'
        }
        return JsonResponse(response_data, status=400)