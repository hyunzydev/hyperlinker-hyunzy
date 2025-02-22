from rest_framework import permissions


class IsOwnerOrHasWritePermission(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.created_by == request.user:
            return True

        return request.user in obj.write_permissions.all()



class IsOwnerOrHasWritePermission(permissions.BasePermission):

    def has_permission(self, request, view):

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.created_by == request.user:
            return True

        if request.method in ["PUT", "PATCH"]:
            return request.user in obj.write_permissions.all()

        if request.method == "DELETE":
            return obj.created_by == request.user

        return False
