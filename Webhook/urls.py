from django.urls import path
from . import views

urlpatterns=[
    path('create_task',views.CreateOrder.as_view()),
    path('get_keys',views.GetSecretKey.as_view())
    
    
]