from rest_framework import serializers
from .models import Rider,ManagementProfile,RiderProfile,Order



class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rider
        fields = ["username","first_name","last_name","email"]

class RiderSerializerProfile(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    id=serializers.SerializerMethodField()
    class Meta:
        model = RiderProfile
        fields = ["id","username","first_name","last_name","email","status"]
    def get_first_name(self,obj):
        return obj.user.first_name
    def get_last_name(self,obj):
            return obj.user.last_name
    def get_email(self,obj):
            return obj.user.email
    def get_username(self,obj):
            return obj.user.username
    def get_id(self,obj):
            return obj.user.pk

class OrderSerializer(serializers.ModelSerializer):
     class Meta:
          model = Order
          fields = ["email","address","mobile"]

class ManagementProfileSerializer(serializers.ModelSerializer):
    Rider = RiderSerializerProfile(many=True)
    Order = OrderSerializer(many=True)
    class Meta:
        model = ManagementProfile 
        fields = ['title','industry',"Rider","Order"]