from django.contrib import admin
from django.urls import path
from video.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view)
]
