from django.shortcuts import render
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from core.models import (
    Examination,
    ExaminationType,
    Patient,
    User,
)
from .serializers import (
    PatientSerializer,
)


class PatientAPI(APIView):
    def get(self, request, format=None):
        user = User.objects.get(Q(id=request.query_params["user_id"]))
        patients = Patient.objects.filter(Q(zone=user.zone)).order_by('-create_time')
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)
