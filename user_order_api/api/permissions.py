from rest_framework.permissions import IsAuthenticated


class IsOrdererOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_staff or obj.user == request.user
        )
