from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import SparePart, SparePartTrace

# 🔹 Unregister the default User & Group
admin.site.unregister(User)
admin.site.unregister(Group)

# 🔹 Re-register with French names
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):
    class Meta:
        verbose_name = "Groupe"
        verbose_name_plural = "Groupes"


# ➕ Classe admin personnalisée pour SparePart
@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'vendor_type', 'stock', 'taux_defaut']

    def taux_defaut(self, obj):
        total = obj.traces.count()
        defectueux = obj.traces.filter(event_description__icontains='defect').count()
        if total == 0:
            return "0%"
        return f"{(defectueux / total) * 100:.1f}%"
    taux_defaut.short_description = 'Taux de défaut'


# ✅ Admin pour SparePartTrace
@admin.register(SparePartTrace)
class SparePartTraceAdmin(admin.ModelAdmin):
    list_display = ['spare_part', 'event_description', 'timestamp']

