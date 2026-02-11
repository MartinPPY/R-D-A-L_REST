from rest_framework import serializers
from .models import *


class EmptySerializer(serializers.Serializer):
    pass

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"

class ActivitySerializer(serializers.ModelSerializer):

    area = AreaSerializer(read_only = True)

    #Para crear,actualizar o borrar actividades
    area_id = serializers.PrimaryKeyRelatedField(
        queryset=Area.objects.all(),
        source="area",
        write_only=True
    )

    class Meta:
        model = Activity
        fields = "__all__"
        read_only_fields = ["user"]


