from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from datetime import date


class EmptySerializer(serializers.Serializer):
    pass

class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id","first_name","last_name"]

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"

class ActivitySerializer(serializers.ModelSerializer):

    area = AreaSerializer(read_only = True)
    user = SimpleUserSerializer(read_only= True)

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
        
    def validate(self,data):
        
        hoy = date.today()
        user = self.context["request"].user
        
        
        actividades_mes = Activity.objects.filter(user=user,fecha__year=hoy.year,fecha__month=hoy.month)
        
        for actividad in actividades_mes:
            if data["hora_inicio"] < actividad.hora_fin and data["hora_fin"] > actividad.hora_inicio and data["fecha"] == actividad.fecha:
                raise serializers.ValidationError("La actividad se superpone con otra actividad del mismo mes.")
        
        return data
    
    

class OrdenPagoSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdenCompra
        fields = "__all__"



