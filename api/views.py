from .models import User,Rider,RiderProfile,Order,ManagementProfile,ManagementManager,Customer,CustomerProfile,Management
from .serializer import ManagementProfileSerializer,RiderSerializerProfile,RiderSerializer,OrderSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status
from django.db.utils import IntegrityError,Error

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

def generate_tokens_for_user(user): 
    serializer = MyTokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token

class Home(APIView):
    def get(self,request):
        management = ManagementProfile.objects.all()
        serializer = ManagementProfileSerializer(management,many=True).data
        return Response(serializer)


class ManagementView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer = ManagementProfileSerializer(instance=request.user.ManagementProfile).data
        return Response(serializer)
    
class CreateRiderView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        firstName = request.data['firstName']
        lastName = request.data['lastName']
        email = request.data['email']
        country = request.data['country']
        city = request.data['city']
        zipCode = request.data['zip']
        mob = request.data['mob']
        password = request.data['password']
        try:
            obj = Rider.objects.create(role="RIDER",username=email.split("@")[0],first_name=firstName,last_name=lastName,email=email,city=city,country=country,zip_code=zipCode,mobile=mob)
            
        except IntegrityError:
            return Response({"msg":"User Email Already Exists"},status=status.HTTP_409_CONFLICT)
        else:
            obj.set_password(password)
            obj.save()
            obj.RiderProfile.management = request.user.ManagementProfile
            obj.RiderProfile.save()
            return Response({"msg":"created"})
    def delete(self,request):
        try:
            obj = Rider.objects.get(pk=request.data["id"])
        except:
            return Response({"msg":"deleted"})
        else:
            obj.delete()
            return Response({"msg":"deleted"})

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
   
        email = request.data['email']
        country = request.data['country']
        city = request.data['city']
        zipCode = request.data['zip']
        mob = request.data['mob']
        status_code = request.data["status"]
        address = request.data["address"]
        try:
            Order.objects.create(email=email,address=address,mobile=mob,zip_code=zipCode,country=country,city=city,management=request.user.ManagementProfile,status=status_code)
        except:
            return Response({"msg":"error"},status=status.HTTP_409_CONFLICT)
        else:
            return Response({"msg":"Order Created"})

class SignInView(APIView):
    def post(self,request):
        email = request.data["email"]
        password = request.data["password"]
        try:
            user = Management.objects.get(email=email)
          
        except Management.DoesNotExist:
            return Response({'msg':"user doesnot Exist"},status=401)
        else:
            if user.check_password(password):
                access_token, refresh_token = generate_tokens_for_user(user)
                return Response({
                    "access":str(access_token),
                    "refresh":str(refresh_token)
                        },status=status.HTTP_200_OK)

            else:
                return Response({'msg':'invalid Password or Email'},status=status.HTTP_401_UNAUTHORIZED)





class SignUpView(APIView):
    def post(self,request):
        email = request.data["email"]
        firstName =  request.data["firstName"]
        lastName = request.data["lastName"]
        password = request.data["password"]
        try:
            user = Management.objects.filter(email=email)
        except user.exists():
            return Response({"msg":"User already exists"})
        else:
            user = Management.objects.create(email=email,username=email.split("@")[0],first_name=firstName,last_name=lastName,role="MANAGEMENT")
            user.set_password(password)
            user.save()
            access_token, refresh_token = generate_tokens_for_user(user)
            return Response({
                "access":str(access_token),
                "refresh":str(refresh_token)
                    },status=status.HTTP_200_OK)

@api_view(["GET"])
def test(resquest):
    obj = User.objects.get(email="burhan@gmail.com")
    print(obj.user)
    return Response({})