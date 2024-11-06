from django.contrib import admin
from django.urls import path, include
from . import home
from . import models



urlpatterns = [
    path('co2_log/', models.co2_log_ListView.as_view()),
    path('co2_rolling_log/', models.co2_rolling_log_ListView.as_view())
]
