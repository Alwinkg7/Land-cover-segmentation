from django.urls import path
from .views import PredictLandCover

urlpatterns = [
    path('predict/', PredictLandCover.as_view(), name='predict_landcover'),
]