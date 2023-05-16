from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
def main(request):
    data = {
        "title": "2022-AIX 해커톤",
        "period": "2022-11-02~2022-11-31"
    }
    return JsonResponse(data)

@csrf_exempt
def submit_data(request):
    if request.method == "POST":
        title = request.POST.get("title")
        period = request.POST.get("period")
        data = {
            "title": title,
            "period": period
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"success": False, "message": "Invalid request method"})