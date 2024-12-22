"""
URL configuration for DB_HealthManagement project.

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
from django.urls import path, include
import DB_HealthManagement.views
import accounts.views

urlpatterns = [
    path('', DB_HealthManagement.views.cover, name='cover'),
    path('about/', DB_HealthManagement.views.about, name='about'),
    path('contact_us/', DB_HealthManagement.views.contact_us, name='contact_us'),
    path('admin/', admin.site.urls),
    path('index/', DB_HealthManagement.views.index, name='index'),
    path('register/', accounts.views.Register.as_view(), name='register'),  # 注册页面
    # path('login/', accounts.views.Login.as_view(), name='login'),  # 登录页面
    path('login/', accounts.views.Login.as_view(), name='login'),  # 登录页面
    path('logout/', accounts.views.user_logout, name='logout'),  # 注销页面
    path('health_profile/', include('health_profile.urls')),
    path('exercise_info/', include('exercise_info.urls')),

]


