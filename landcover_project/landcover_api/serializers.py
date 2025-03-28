from rest_framework import serializers
from .models import LandCoverImage

class LandCoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandCoverImage
        fields = ['id', 'image', 'uploaded_at']