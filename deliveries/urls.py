from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    #path('resolve-address/', views.resolve_address),
    path('timeslots/', views.get_available_timeslots),
    path('new_user/', views.create_new_user),
    path('deliveries/', views.book_new_delivery),
    path('deliveries/<int:delivery_id>/complete', views.mark_complete),
    path('deliveries/<int:delivery_id>', views.delete_delivery),
    path('deliveries/daily', views.get_daily_deliveries),
    path('deliveries/weekly', views.get_weekly_deliveries),

]
