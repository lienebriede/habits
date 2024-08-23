from django.contrib import admin
from .models import Coupling


@admin.register(Coupling)
class CouplingAdmin(admin.ModelAdmin):
    list_display = ('owner', 'habit1', 'habit2')
    search_fields = ('habit1__name', 'habit2__name', 'owner__username')
