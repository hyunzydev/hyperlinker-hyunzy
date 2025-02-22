from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import WebLink  # ✅ WebLink 모델 가져오기


from .models import WebLink  # ✅ WebLink 모델 가져오기

User = get_user_model()


class WebLinkSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    shared_with = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=False
    )
    write_permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=False
    )

    class Meta:
        model = WebLink
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
