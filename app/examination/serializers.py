from rest_framework import serializers
from core.models import (
    Examination,
    ExaminationType,
)


class ExaminationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExaminationType
        fields = (
            "id",
            "name",
            "create_time",
        )


class ExaminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examination
        fields = (
            "id",
            "output_image",
            "create_time",
        )