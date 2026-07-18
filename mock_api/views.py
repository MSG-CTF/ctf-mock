from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health(request):
    # sentinel이 mock 서버 자체가 살아있는지 먼저 확인할 때 사용하는 기본 응답이다.
    return Response(
        {
            "status": "healthy",
            "service": "ctf-mock",
            "checkedAt": timezone.now().isoformat(),
        }
    )
