from rest_framework import permissions

class IsAdminOrCoordinator(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'admin' or request.user.role == 'coordinator')

class IsTaskOwnerOrAdminOrCoordinator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Admins or coordinators can view/edit any task
        if request.user.role in ['admin', 'coordinator']:
            return True
        # Task owners can view/edit their own tasks
        return obj.assigned_to == request.user
