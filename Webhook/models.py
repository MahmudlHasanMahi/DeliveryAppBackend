from django.db import models
from api.models import Management
from django.utils.crypto import get_random_string
import secrets
# Create your models here.

def unique_key():
        return get_random_string(64)

# def generate_secret_key():
#         return get_random_string(64)
def generate_api_key():
        return secrets.token_urlsafe(64)

class Webhook(models.Model):
        Management = models.OneToOneField(Management,related_name="Webhook",null=False,blank=False,on_delete=models.CASCADE)
        secret_key = models.CharField(max_length=64,default=unique_key,blank=False,null=False,unique=True,editable=False)
        api_key = models.CharField(max_length=64,default=generate_api_key,blank=False,null=False,unique=True,editable=False)
        created = models.DateTimeField(auto_now_add=True)
        activated = models.BooleanField(default=True,null=False,blank=False)
        def __str__(self):
                return f'WebhookID#{self.id}'
        


