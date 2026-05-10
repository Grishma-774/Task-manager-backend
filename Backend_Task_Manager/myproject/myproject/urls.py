"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

from task_manager.views import Register_view,Create_view,Get_View,Profile_View,Notification_view,Notification_read

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/',Register_view.as_view()),
    path('api/token/',TokenObtainPairView.as_view()),
    path('api/token/refresh/',TokenRefreshView.as_view()),
    path('create_task/',Create_view.as_view()),
    path('get_task/<int:pk>',Get_View.as_view()),
    path('profile/',Profile_View.as_view()),
    path('notification/',Notification_view.as_view()),
    path('notification_read/',Notification_read.as_view())

]
