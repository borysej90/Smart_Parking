from django.urls import path
from . import views

urlpatterns = [
    path('sites/<int:site_id>/lots/', views.ParkingList.as_view(), name='parking-lots'),
    path('sites/<int:site_id>/lots/<int:pk>/', views.ParkingDetail.as_view(), name='parking-lot')
]