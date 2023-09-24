from django.shortcuts import render
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils import maskrcnn_predict
from rest_framework.views import APIView
from django.db.models import Q
from core.models import (
    Examination,
    ExaminationType,
    Patient,
    User,
)
from .serializers import (
    ExaminationSerializer,
)


class ExaminationAPI(APIView):
    def get(self, request, format=None):
        examinations = Examination.objects.filter(Q(user=request.query_params["user_id"])).order_by('-create_time')
        serializer = ExaminationSerializer(examinations, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def savefile(request):
    file = request.FILES['file']
    file_name = default_storage.save(file.name, file)
    examination = Examination()
    input_image = file_name
    with open('images/inputs/' + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    output_image = maskrcnn_predict.single_process_csa("images/inputs/" + file.name)
    with open("images/outputs/" + output_image, 'rb') as local_file:
        default_storage.save(output_image, local_file)
    examination.input_image = input_image
    examination.output_image = output_image
    print(request.data["user_id"])
    examination.user = User.objects.get(Q(id=request.data["user_id"]))
    examination.patient = Patient.objects.get(Q(id=1))
    examination.examination_type = ExaminationType.objects.get(Q(id=3))
    examination.result = "1,4,5"
    examination.save()
    return Response(111)