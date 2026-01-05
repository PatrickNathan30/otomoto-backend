from rest_framework import permissions

class EstVendeurOuLectureSeule(permissions.BasePermission):
    """
    Permission personnalisée :
    - Les méthodes sûres (GET, HEAD, OPTIONS) sont toujours autorisées.
    - Les méthodes d’écriture nécessitent que l’utilisateur appartienne au groupe 'Vendeur'.
    """

    def has_permission(self, request, view):
        # ✅ Autoriser toutes les requêtes en lecture seule
        if request.method in permissions.SAFE_METHODS:
            return True

        # ✅ Vérifier que l’utilisateur est authentifié
        if not request.user or not request.user.is_authenticated:
            return False

        # ✅ Vérifier que l’utilisateur appartient au groupe "Vendeur"
        return request.user.groups.filter(name="Vendeur").exists()


