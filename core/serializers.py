from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from .services import check_activity_overlap
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
        
    def validate(self, data):
        user = self.context["request"].user

        fecha = data.get("fecha", self.instance.fecha if self.instance else None)
        hora_inicio = data.get("hora_inicio", self.instance.hora_inicio if self.instance else None)
        hora_fin = data.get("hora_fin", self.instance.hora_fin if self.instance else None)

        # Validación de seguridad: Asegurarse de que tenemos todos los datos necesarios
        if not fecha or not hora_inicio or not hora_fin:
            raise serializers.ValidationError("Faltan datos requeridos para validar la actividad.")
        
        # Obtenemos el ID para excluirlo de la validación si estamos editando
        exclude_id = self.instance.id if self.instance else None
        
        # MEJORA: Usar capa de servicio para validar superposición
        if check_activity_overlap(
            user=user,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            exclude_id=exclude_id
        ):
            raise serializers.ValidationError("La actividad se superpone con otra actividad del mismo día.")
        
        return data
    
    

class OrdenPagoSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrdenCompra
        fields = "__all__"

# SERIALIZERS PARA DOCUMENTACIÓN SWAGGER
class ResumenUsuarioResponseSerializer(serializers.Serializer):
    horas_acumuladas = serializers.IntegerField()
    total_acumulado = serializers.IntegerField()
    horas_aprobadas = serializers.IntegerField()
    orden_compra = serializers.IntegerField(allow_null=True)

class ResumenMensualAdminResponseSerializer(serializers.Serializer):
    usuarios = serializers.IntegerField()
    cantidad_horas = serializers.IntegerField()
    cantidad_orden_compra = serializers.IntegerField()

class ResumenOrdenCompraItemSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    usuario = serializers.CharField()
    monto_acumulado = serializers.IntegerField()
    orden_compra = serializers.IntegerField(allow_null=True)
