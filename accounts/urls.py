from django.urls import path
from . import views
urlpatterns = [
    path('',views.user_login,name='login'),
    path('register/',views.user_register,name='register'),
    path('forgetpassword/',views.forgetpassword,name='forgetpassword'),
    path('logout/',views.logout,name='logout'),

]