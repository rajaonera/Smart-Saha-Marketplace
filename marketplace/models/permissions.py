from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Autorise la modification uniquement au propriétaire de l'objet.
    """

    def has_object_permission(self, request, view, obj):
        # Autorisation en lecture : GET, HEAD, OPTIONS sont toujours autorisés
        if request.method in permissions.SAFE_METHODS:
            return True

        # Autorisation d'édition uniquement si l'utilisateur est le propriétaire
        return obj.user == request.user
