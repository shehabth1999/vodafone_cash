from rest_framework import status
from rest_framework.response import Response
from django.utils.translation import gettext as _

class MainResponse(object):
    def __init__(self):
        self.POST = 1
        self.PUT = 2
        self.DELETE = 3
        self.RETREIVE = 4

    def returnReponse(self,message="",status=True,code=status.HTTP_200_OK,body={},action=1):
            if action == self.POST:
                message = _("Created Successfully")
            if action == self.PUT:
                message = _("Edit Successfully")
            if action == self.DELETE:
                message =_("Delete Successfully")
            if action == self.RETREIVE:
                message = _("Receive Successfully")
            
            return Response(
                {
                "message": message,
                "status":  status,
                "code":code,
                "body":body
                },status=code)

