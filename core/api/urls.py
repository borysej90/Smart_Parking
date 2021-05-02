from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from . import views

processors_urls = [
    path('map/', views.get_parking_lots_map, name='get-parking-lots-map'),
    path('rtsp/', views.get_camera_stream_url, name='get-camera-stream-url'),
    path('lots/', views.update_processors_parking_lots, name='update-processors-parking-lots')
]

sites_router = DefaultRouter()
sites_router.register('sites', views.ParkingSiteViewSet, basename='parking-sites')

lots_router = NestedDefaultRouter(sites_router, 'sites', lookup='site')
lots_router.register('lots', views.ParkingLotViewSet, basename='parking-lots')

urlpatterns = [
    *sites_router.urls,
    *lots_router.urls,
    path('processors/<int:processor_id>/', include(processors_urls)),
]
