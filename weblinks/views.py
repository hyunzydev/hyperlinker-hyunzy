
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import WebLink
from .serializers import WebLinkSerializer, UserSerializer
from .permissions import IsOwnerOrHasWritePermission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from weblinks.models import WebLink
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from weblinks.models import WebLink
from django.contrib.auth import get_user_model



User = get_user_model()


class WebLinkViewSet(viewsets.ModelViewSet):


    serializer_class = WebLinkSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrHasWritePermission,
    ]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return WebLink.objects.filter(created_by=user) | WebLink.objects.filter(
            shared_with=user
        )

    def partial_update(self, request, pk=None):
        web_link = get_object_or_404(WebLink, id=pk)

        if (
            web_link.created_by != request.user
            and request.user not in web_link.write_permissions.all()
        ):
            return Response(
                {"error": "수정 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(web_link, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], url_path="share")
    def share_link(self, request, pk=None):
        web_link = self.get_object()

        if web_link.created_by != request.user:
            return Response(
                {"error": "공유할 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )

        user_ids = request.data.get("users", [])
        write_permission = request.data.get("write", False)

        users = User.objects.filter(id__in=user_ids)
        web_link.shared_with.add(*users)

        if write_permission:
            web_link.write_permissions.add(*users)

        return Response(
            {
                "message": "공유 성공!",
                "shared_users": [user.username for user in users],
            },
            status=status.HTTP_200_OK,
        )


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def search_weblinks(request):
    query = request.GET.get("q", "")
    weblinks = WebLink.objects.filter(created_by=request.user)

    if query:
        weblinks = weblinks.filter(
            Q(name__icontains=query)
            | Q(url__icontains=query)
            | Q(category__icontains=query)
        )

    serializer = WebLinkSerializer(weblinks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)



@csrf_exempt
@login_required
def share_weblink(request, weblink_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            permission = data.get("permission")

            if not user_id or not permission:
                return JsonResponse({"error": "잘못된 요청"}, status=400)

            weblink = get_object_or_404(WebLink, id=weblink_id)

            if weblink.created_by != request.user:
                return JsonResponse({"error": "공유할 권한이 없습니다."}, status=403)

            user = get_object_or_404(User, id=user_id)

            if user in weblink.shared_with.all():
                return JsonResponse(
                    {"message": "이미 공유된 사용자입니다."}, status=200
                )

            weblink.shared_with.add(user)

            if permission == "write":
                weblink.write_permissions.add(user)

            return JsonResponse(
                {
                    "message": "공유 성공!",
                    "shared_with": list(
                        weblink.shared_with.values("id", "username")
                    ),
                },
                status=200,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "잘못된 요청"}, status=400)
