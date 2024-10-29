from django.urls import path,include
from . import views

urlpatterns = [
    path('interview/', views.index, name='interview'),
]

