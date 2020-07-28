from django.shortcuts import render
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView


class FileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)
