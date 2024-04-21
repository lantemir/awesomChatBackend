from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django_app import models
from django.core.paginator import Paginator
from django_app import serializers

def index(request):
    return JsonResponse({"response": "Ok!"})

def users(request):
    return JsonResponse({"response": "OK!"})

@api_view(http_method_names=["GET", "POST", "PATCH", "DELETE", "OPTIONS"])
def chat(request, sms_id=None):
    try:
        if sms_id:
            if request.method == "GET":
                return Response(status = status.HTTP_200_OK)
            elif request.method == "POST":
                return Response(status = status.HTTP_200_OK)
            else:
                return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            if request.method == "GET":
                page = int(request.GET.get("page", 1))
                limit = int(request.GET.get("limit", 3))

                obj_list = models.TextModel.objects.all()      
                paginator_obj = Paginator(object_list=obj_list, per_page=limit)
                current_page = paginator_obj.get_page(page).object_list
                serialized_obj_list = serializers.TextModelSerializer(isinstance=current_page, many=True).data                

                return Response(data={"list": serialized_obj_list, 
                                      "x-total-count": len(obj_list)}, status = status.HTTP_200_OK)
            elif request.method == "POST":
                text = int(request.GET.get("text", ""))
                if text:
                    models.TextModel.objects.create(
                        text = text

                    )
                    return Response(status = status.HTTP_201_CREATED)
                return Response(status = status.HTTP_204_NO_CONTENT)
            else:
                return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as error:
        print(error)
        return Response(status= status.HTTP_500_INTERNAL_SERVER_ERROR)
       

