from django.urls import path

from . import views

urlpatterns = [
    path('sites/<int:site_id>/lots/', views.ParkingList.as_view(), name='parking-lots'),
    path('sites/<int:site_id>/lots/<int:pk>/', views.ParkingDetail.as_view(), name='parking-lot'),
    path('processors/<int:processor_id>/map/', views.get_parking_lots_map, name='get-parking-lots-map'),
    path('processors/<int:processor_id>/rtsp/', views.get_camera_stream_url, name='get-camera-stream-url')
]
