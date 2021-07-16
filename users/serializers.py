from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from django.contrib.auth import get_user_model


class UsersSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        
        fields = [
            'pk', 
            'first_name', 
            'last_name', 
            'username'
        ]
        
        read_only_fields = [
            'pk',
        ]