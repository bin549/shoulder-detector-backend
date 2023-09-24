from rest_framework import serializers
from core.models import (
    Examination
)



class ExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examination
        fields = (
            "id",
            "output_image",
        )