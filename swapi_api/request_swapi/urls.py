from django.urls import path
from request_swapi.views import (StoreData,
                                 PlanetCreateView, 
                                 PlanetDetailView, 
                                 PlanetUpdateView, 
                                 PlanetDeleteView, 
                                 PlanetListView)

urlpatterns = [
    path('api/v1/query-store/', StoreData.as_view(), name='query-store-data'),
    path('api/v1/planets/', PlanetListView.as_view(), name='planet-list'),
    path('api/v1/planets/create/', PlanetCreateView.as_view(), name='planet-create'),
    path('api/v1/planets/<int:pk>/', PlanetDetailView.as_view(), name='planet-detail'),
    path('api/v1/planets/<int:pk>/update/', PlanetUpdateView.as_view(), name='planet-update'),
    path('api/v1/planets/<int:pk>/delete/', PlanetDeleteView.as_view(), name='planet-delete'),
]