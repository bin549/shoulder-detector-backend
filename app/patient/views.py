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
    Zone,
)
from .serializers import (
    PatientSerializer,
)
from django.core.paginator import Paginator
from django.http import JsonResponse


class PatientAPI(APIView):
    def get(self, request, format=None):
        user = User.objects.get(Q(id=request.query_params["user_id"]))
        patients = Patient.objects.filter(Q(zone=user.zone)).order_by('create_time')
        total_size = len(patients)
        if request.query_params.__contains__("limit"):
            paginator = Paginator(patients, per_page=request.query_params["limit"])
            page = paginator.get_page(request.query_params["page"])
            patients = page.object_list
        serializer = PatientSerializer(patients, many=True)
        result = {
            "list": serializer.data,
            "total_size": total_size,
        }
        return JsonResponse(result)

    def post(self, request, format=None):
        patient = Patient()
        patient.name = request.data["name"]
        # zone = Zone.objects.get(Q(id=request.data["zone_id"]))
        user = User.objects.get(Q(id=request.data["user_id"]))
        zone = Zone.objects.get(Q(id=user.zone.id))
        patient.zone = zone
        patient.save()
        return Response(1)

    def delete(self, request, format=None):
        patient = Patient.objects.get(Q(id=request.data["id"]))
        Examination.objects.filter(Q(patient=patient.id)).delete()
        patient.delete()
        return Response(1)
