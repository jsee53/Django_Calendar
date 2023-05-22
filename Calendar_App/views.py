from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
    
@csrf_exempt
def main(request):
    if request.method == 'POST':
        # POST 요청의 경우 처리 로직을 구현합니다.
        try:
            data = json.loads(request.body)
            title = data['title']
            date = data['date']
            
        # 여기에서 받은 title과 date 값을 활용하여 원하는 로직을 수행합니다.
        # 예를 들어, 데이터베이스에 저장하거나 다른 처리를 수행할 수 있습니다.
            
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
        # POST 요청의 경우 처리 로직을 구현합니다.
        try:
            data = json.loads(request.body)
            id = data['id']
            password = data['password']
            
            # 여기에서 받은 id와 password 값을 활용하여 원하는 로직을 수행합니다.
            # 예를 들어, 데이터베이스에 저장하거나 다른 처리를 수행할 수 있습니다.
            
            # 응답 데이터를 만들어 클라이언트에게 전송합니다.
            response_data = {
                'id': id,
                'password': password,
                'message': '로그인 성공!',
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
