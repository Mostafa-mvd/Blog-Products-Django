from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):
    created_time = serializers.SerializerMethodField()
    creator = serializers.SlugRelatedField(
        queryset=get_user_model().objects.all(), slug_field="username"
    )

    category = serializers.SlugRelatedField(
        queryset=models.Post.objects.all(), slug_field="name"
    )

    class Meta:
        model = models.Post
        fields = [
            "created_time",
            "title",
            "category",
            "creator",
            "like",
            "dislike",
            "body",
        ]

    # get_<field_name> -> we defined field_name (created_time) at the top of code
    def get_created_time(self, obj):
        return obj.created_time.strftime('%B %d %Y - %H:%M:%S')
