from rest_framework import serializers
from core.models import (
    Patient
)



class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            "id",
            "name",
            "get_image",
            "create_time",
        )