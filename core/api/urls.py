from django.urls import include, path

from . import views

processors_urls = [
    path('map/', views.get_parking_lots_map, name='get-parking-lots-map'),
    path('rtsp/', views.get_camera_stream_url, name='get-camera-stream-url'),
    path('lots/', views.update_processors_parking_lots, name='update-processors-parking-lots')
]

sites_urls = [
    path('', views.ParkingSiteViewSet.as_view({'get': 'list', 'post': 'create'}), name='parking-sites'),
    path('<int:pk>/', views.ParkingSiteViewSet.as_view({'get': 'retrieve',
                                                        'put': 'update',
                                                        'patch': 'partial_update',
                                                        'delete': 'destroy'}), name='parking-site'),
]

lots_urls = [
    path('', views.ParkingList.as_view(), name='parking-lots'),
    path('<int:pk>/', views.ParkingDetail.as_view(), name='parking-lot'),
]

urlpatterns = [
    path('sites/', include(sites_urls)),
    path('sites/<int:site_id>/lots/', include(lots_urls)),
    path('processors/<int:processor_id>/', include(processors_urls)),
]
