from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver




class User(AbstractUser):
    email = models.CharField(max_length=250,unique=True,null=False,blank=False)
    ROLE = [
        ('NONE','None'),
        ('MANAGEMENT', 'Management'),
        ('RIDER', 'Rider'),
        ('CUSTOMER', 'Customer'),
    ]
    role = models.CharField(max_length=15,choices=ROLE,default="NONE")
    address = models.CharField(max_length=1024,blank=True,null=True)
    mobile = models.IntegerField(blank=True,null=True,unique=True)
    zip_code = models.CharField(max_length=12,null=True)
    country = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    created = models.DateTimeField(auto_now_add=True)


class ManagementManager(BaseUserManager):
    
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(role="MANAGEMENT")
    

class Management(User):
    objects = ManagementManager()
    class Meta:
        proxy = True


@receiver(post_save, sender=Management)
def create_user_profile(sender,instance,created,**kwargs):
    if created and instance.role == "MANAGEMENT":
        ManagementProfile.objects.create(user=instance)   

class ManagementProfile(models.Model):
    user = models.OneToOneField(User,limit_choices_to={'role': "MANAGEMENT"},related_name="ManagementProfile",on_delete=models.CASCADE)
    title = models.TextField(max_length=250,unique=True,null=True,blank=True)
    industry = models.TextField(max_length=250,null=True,blank=True)

class ManagerRider(BaseUserManager):
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(role="RIDER")
    
class Rider(User):
    objects = ManagerRider()
    class Meta:
        proxy = True


@receiver(post_save, sender=Rider)
def create_user_profile(sender,instance,created,**kwargs):
    if (created and instance.role == "RIDER"):
        RiderProfile.objects.create(user=instance) 

class RiderProfile(models.Model):
    user = models.OneToOneField(User,limit_choices_to={'role': "RIDER"}, related_name="RiderProfile",on_delete=models.CASCADE)
    management = models.ForeignKey(ManagementProfile,null=True,on_delete=models.CASCADE,related_name="Rider")
    STATUS_CHOICE = [
                    ("NONE","None"),
                    ("FREE","Free"),
                    ("BUSY","Busy"),
                    ]
         
    status = models.CharField(max_length=15,choices=STATUS_CHOICE,default="NONE")

class ManagerCustomer(BaseUserManager):
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(role="CUSTOMER")    
class Customer(User):
    objects = ManagerCustomer()
    class Meta:
        proxy = True


@receiver(post_save,sender=Customer)
def create_user_profile(instance,created, **kwargs):
    if created and instance.role == "CUSTOMER":
        CustomerProfile.objects.create(user=instance)

class CustomerProfile(models.Model):
    user = models.OneToOneField(User,limit_choices_to={"role":"CUSTOMER"},related_name="CustomerProfile",on_delete = models.CASCADE)

class Order(models.Model):
    email = models.CharField(max_length=250,null=True,blank=True)
    address = models.CharField(max_length=1024,blank=True,null=True)
    mobile = models.IntegerField(blank=True,null=True,unique=True)
    zip_code = models.CharField(max_length=12,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,blank=True)
    management = models.ForeignKey(ManagementProfile,on_delete=models.CASCADE,related_name="Order")
    customer = models.ForeignKey(CustomerProfile,null=True,blank=True,on_delete=models.SET_NULL,related_name='Order')
    rider = models.ForeignKey(RiderProfile,limit_choices_to={'status': "FREE"},null=True,blank=True,on_delete=models.SET_NULL,related_name='Order')
    STATUS_CHOICE = [
                    ("NONE","None"),
                    ("DELIVERED","Delivered"),
                    ("NOT_DELIVERED","Not Delivered")
                    ]
    
    status = models.CharField(max_length=15,choices=STATUS_CHOICE,default="NONE")
    Type = models.TextField(max_length=250,null=True,blank=True)

        
    

@receiver(post_save,sender=Order)
def create_user_profile(sender,instance,created, **kwargs):

    user = User.objects.filter(email=instance.email)
    if created:
        if user.exists():
            customer = CustomerProfile.objects.get(user=user.get())
            order = Order.objects.filter(pk=instance.pk).update(customer=customer)
            if customer.mobile != instance.mobile:
                customer['mobile'] = instance.mobile
                customer.save()

        else:
            user = User.objects.create_user(email=instance.email,address=instance.address,mobile=instance.mobile,
                                    zip_code = instance.zip_code,country=instance.country,city=instance.city,
                                    role="CUSTOMER",username=instance.email.split("@")[0])
            customer = CustomerProfile.objects.create(user=user)
            Order.objects.filter(pk=instance.pk).update(customer=customer)

