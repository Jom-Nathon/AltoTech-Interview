from django.urls import path
from .views import *

urlpatterns = [
    path('hotels/', get_all_hotels, name='get_all_hotels'),
    path('hotels/<str:hotel_id>/floors/', get_floors_from_hotel, name='get_floors_from_hotel'),
    path('floors/<str:floor_id>/rooms/', get_rooms_from_floor, name='get_rooms_from_floor'),
    path('rooms/<str:room_id>/data/', get_room_data, name='get_room_data'),
    path('rooms/<str:room_id>/data/life_being/', get_life_being, name='get_life_being'),
    path('rooms/<str:room_id>/data/iaq/', get_iaq, name='get_iaq'),
    path('hotels/<str:hotel_id>/energy_summary/', get_energy_summary, name='get_energy_summary'),
    path('chat/', chat_endpoint, name='chat'),
]


