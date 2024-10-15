from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from django.utils.translation import gettext as _


class HelloApiView(APIView):
    def get(self, request: Request) -> Response:
        return Response(
            {"message": "{}!".format(_("Hello World"))})
