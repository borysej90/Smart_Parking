from django.urls import path
from . import views

urlpatterns = [
    path('parking-lots/', views.process_parking_lots, name='parking-lots'),
    path('parking-lots/<int:pk>/', views.process_parking_lot, name='parking-lot')
]