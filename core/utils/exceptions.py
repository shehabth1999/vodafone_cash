from rest_framework.views import exception_handler
from core.utils.response import MainResponse
from rest_framework.exceptions import AuthenticationFailed

def custom_exception_handler(exc, context):
    try:
        print("just exception handler") 
        response = exception_handler(exc, context)
        print(response)
        if response is not None and response.status_code == 400:
            response = MainResponse().returnReponse(
                message="عفواً الإستجابه غير متوقعه",
                code=response.status_code ,
                action=6,
                status=False
            )

        if response is not None and response.status_code == 401:
            response  = MainResponse().returnReponse(
                message=AuthenticationFailed.default_detail,
                code=response.status_code ,
                action=6,
                status=False
            )
        
        if response is not None and response.status_code == 403:
            response = MainResponse().returnReponse(
                message="عفواً لا يمكنك الوصول",
                code=response.status_code ,
                action=6,
                status=False
            )
        
     

        if response is not None and response.status_code == 404:
            response = MainResponse().returnReponse(
                message="عفواً المسار غير معروف",
                code=response.status_code ,
                action=6,
                status=False
            )
            
        if response is not None and response.status_code == 409:
            response = MainResponse().returnReponse(
                message="عفواً حدث تعارض فى البيانات حاول مره اخرى",
                code=response.status_code ,
                action=6,
                status=False
            )
 
        if response is not None and response.status_code == 500:
            response = MainResponse().returnReponse(
                message="عفواً يوجد مشكله فى  الخادم",
                code=response.status_code ,
                action=6,
                status=False
            )



        # if response.status_code == 405:
        #     response.data = {  
        #         "message": exc.detail ,  
        #         "status":  False,  
        #     }

        # if response.status_code == 400:
        #     data = dict(exc.detail)
        #     if(str( type(data)) == "<class 'dict'>"):

        #         for i in data.keys():

        #             data2 = data[i]
        #             if(str( type(data2)) == "<class 'dict'>"):

        #                 for m in data2.keys():
        #                     response.data = {  
        #                             "message": str(data2[m][0] ),  
        #                             "status":  False,  
        #                         }
        #             else:
        #                 response.data = {  
        #                             "message": str(data[i][0] ),  
        #                             "status":  False,  
        #                         }


    except Exception as e:
        print(e)
        return response
    return response