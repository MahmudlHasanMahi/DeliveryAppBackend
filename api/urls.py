from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
urlpatterns = [
    path('', views.Home.as_view()),
    path('management/signin', views.SignInView.as_view()),
    path('test',views.test.as_view()),
    path("management/RefreshToken",TokenRefreshView.as_view()),
    path("management/signup", views.SignUpView.as_view()),
    path("createRider",views.CreateRiderView.as_view()),
    path("management",views.ManagementView.as_view()),
    path("CreateOrder",views.CreateOrderView.as_view()),

]