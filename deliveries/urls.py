from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('couriers/', views.courier_list),
    path('resolve-address/', views.resolve_address)
]
