from .models import CustomeField, User
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        return token

class EmployeeCreationSerializer(serializers.ModelSerializer):
    custome_field=serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = '__all__'

    def get_custome_field(self,obj):
        user=CustomeField.objects.filter(user__id=obj.id)
        detial=EmployeeCustomSerializer(user,many=True)
        return detial.data


class EmployeeCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomeField
        fields='__all__'