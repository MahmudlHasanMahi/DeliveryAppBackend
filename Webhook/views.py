from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.views import test 
from django.utils.crypto import get_random_string,constant_time_compare
from .models import Webhook
import secrets
# Create your views here.

class GetSecretKey(APIView):
    def get(self,request):
        secret_key = get_random_string(64)
        api_key = secrets.token_urlsafe(64)
        return Response({"secret_key":secret_key, "api_key":api_key})

class Get_Delivery_Url(APIView):
    pass

class CreateOrder(test):

    def get(self,request,**kwargs):
        try:
            params = request.GET.dict()
            id,key = params["U"],params["apiKey"]
            webhook = Webhook.objects.get(id=id).api_key
        except:
            return Response({"msg":"Invalid Parameters"})
        else:
            if webhook == key:
                return Response({"msg":"key Matched"})
            else:
                return Response({"msg":"key Unmatched"})
    


