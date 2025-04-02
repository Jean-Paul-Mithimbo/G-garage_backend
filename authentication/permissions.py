from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
     """
    Permission permettant uniquement aux administrateurs d'accéder à la ressource.
    """
     def has_permission(self, request, view):
          return request.user and request.user.is_authentificated and request.user.is_staff
     
class IsMechanic(permissions.BasePermission):
    """
    Permission permettant uniquement aux mécaniciens d’accéder à certaines ressources.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == "mecanicien"

class IsFinanceManager(permissions.BasePermission):
    """
    Permission permettant uniquement aux gestionnaires financiers d’accéder aux ressources de la finance.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == "comptable"