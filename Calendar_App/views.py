from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def main(request):
    if request.method == 'POST':
        # POST 요청의 경우 처리 로직을 구현합니다.
        title = request.POST.get('title')
        date = request.POST.get('date')
        
        # 여기에서 받은 title과 date 값을 활용하여 원하는 로직을 수행합니다.
        # 예를 들어, 데이터베이스에 저장하거나 다른 처리를 수행할 수 있습니다.
        
        # 응답 데이터를 만들어 클라이언트에게 전송합니다.
        response_data = {
            'message': '게시물이 추가되었습니다.',
        }
        return JsonResponse(response_data)
    else:
        # POST 요청이 아닌 경우 예외 처리를 수행하거나 다른 로직을 구현할 수 있습니다.
        response_data = {
            'message': '잘못된 요청입니다.'
        }
        return JsonResponse(response_data, status=400)
