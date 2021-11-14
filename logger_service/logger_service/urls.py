from django.contrib import admin
from django.urls import path, include
from logger import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.log, name='log'),
]
