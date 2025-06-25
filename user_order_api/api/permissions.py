from rest_framework.permissions import BasePermission


class IsOrdererOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_staff or obj.user == request.user
        )
