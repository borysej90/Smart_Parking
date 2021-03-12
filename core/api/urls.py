from django.urls import include, path

from . import views

processors_urls = [
    path('map/', views.get_parking_lots_map, name='get-parking-lots-map'),
    path('rtsp/', views.get_camera_stream_url, name='get-camera-stream-url'),
    path('lots/', views.update_processors_parking_lots, name='update-processors-parking-lots')
]

sites_urls = [
    path('lots/', views.ParkingList.as_view(), name='parking-lots'),
    path('lots/<int:pk>/', views.ParkingDetail.as_view(), name='parking-lot'),
]

urlpatterns = [
    path('sites/<int:site_id>/', include(sites_urls)),
    path('processors/<int:processor_id>/', include(processors_urls)),
]
