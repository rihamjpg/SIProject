from rest_framework import permissions

class IsHRManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_hr

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager

class IsEmployeeOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'employe'):
            return obj.employe.id == request.user.id
        return obj.id == request.user.id

class CanManageService(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_hr or request.user.is_manager

class CanManageContracts(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_hr

class CanProcessSalaries(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_hr

class CanManageRecrutement(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_hr

class CanManageEvaluations(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_hr or request.user.is_manager

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.employe.id == request.user.id or request.user.is_hr
        return request.user.is_hr or request.user.is_manager

class CanApproveLeaves(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_hr or request.user.is_manager

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.employe.id == request.user.id
        return request.user.is_hr or request.user.is_manager

class CanManageFormations(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_hr

class CanManagePointages(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.employe.id == request.user.id
        return request.user.is_hr or request.user.is_manager

class CanManageDocuments(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if obj.confidentialite == 'PUBLIC':
            return True
        if obj.confidentialite == 'PRIVE':
            return obj.employe.id == request.user.id
        return request.user.is_hr