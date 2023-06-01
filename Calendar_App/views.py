from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import pyodbc
    
@csrf_exempt
def main(request):
    if request.method == 'POST':
        # POST 요청의 경우 처리 로직을 구현합니다.
        try:
            data = json.loads(request.body)
            title = data['title']
            date = data['date']
            
            # 응답 데이터를 만들어 클라이언트에게 전송합니다.
            response_data = {
                'title':title,
                'date':date,
                'message': '게시물이 추가되었습니다.',
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
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data['id']
            password = data['password']

            # 데이터 베이스 연동            
            # 아이디와 비밀번호 일치 여부 확인
            db = pyodbc.connect(DSN='Tibero6', uid='sys', pwd='tibero')
            curs = db.cursor()
            
            sql = "SELECT id FROM Users WHERE user_id = ? AND password = ?"
            curs.execute(sql, (user_id, password))
            row = curs.fetchone()
            if row:
                # 로그인 성공 처리 및 추가 작업 수행
                user_key = row[0]
                success_login=True
            else:
                # 로그인 실패 처리
                success_login=False

            curs.close()
            db.close()

            # 응답 데이터를 만들어 클라이언트에게 전송합니다.
            schedule_data = [
                {'date': '2023-05-23', 'title': '일정 1'},
                {'date': '2023-05-23', 'title': '일정 2'},
                {'date': '2023-05-24', 'title': '일정 3'},
            ]
            response_data = {
                'schedule_data': schedule_data,
                'login_result': success_login,
                'user_key': user_key,
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
            db = pyodbc.connect(DSN='Tibero6', uid='sys', pwd='tibero')
            curs = db.cursor()

            # 데이터 입력
            sql = "INSERT INTO Users (id, user_id, password, user_name, date_of_birth, email) VALUES (SEQ_ID.NEXTVAL, ?, ?, ?, ?, ?)"
            curs.execute(sql, (id, password, name, birthDate, email))
            db.commit()  # 변경 사항 커밋

            curs.close()
            db.close()

            successSignup=True; #회원가입 성공 시 true, 실패 시 false 가 되는 로직을 수행
            # 응답 데이터를 만들어 클라이언트에게 전송합니다.
            response_data = {
                'successSignup' : successSignup,
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
            date = data['date']
            
            # 여기에서 받은 date 값을 활용하여 원하는 로직을 수행합니다.
            # 예를 들어, 데이터베이스에 저장하거나 다른 처리를 수행할 수 있습니다.

            schedule_data = [
                {'date': '2023-05-27', 'title': '2023-AIX 해커톤'},
                {'date': '2023-05-27', 'title': '네이버웹툰 지상 최대 공모전'},
                ]
            
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