from django.contrib import admin
from .models import Klientas, Objektas, Profilis  #, ObjektasReview


class ObjektasInline(admin.TabularInline):
    model = Objektas
    extra = 0
#

class KlientasAdmin(admin.ModelAdmin):
    list_display = ['vardas', 'pavarde', 'adresas']
    # inlines = [ObjektasInline]
# #
# #
class ObjektasAdmin(admin.ModelAdmin):
    list_display = ['adresas', 'eso_galia', 'saules_galia', 'akumuliatoriaus_talpa', 'elektromobilio_talpa', 'user',
                    'status', 'vaizdelis']
    list_filter = ['user']
    # list_editable = ['adresas', 'eso_galia', 'saules_galia', 'akumuliatoriaus_talpa', 'elektromobilio_talpa', 'user',
    #                 'status']
    search_fields = ['user']
    fieldsets = (
        ('Vartotojas', {'fields': ('user', 'adresas', 'klientas')}),
        ('Galingumai',
         {'fields': ('eso_galia', 'saules_galia', 'akumuliatoriaus_talpa', 'elektromobilio_talpa', 'status', 'vaizdelis')}),
    )
    # inlines = [ObjektasInline]


# Register your models here.
admin.site.register(Klientas, KlientasAdmin)
admin.site.register(Objektas, ObjektasAdmin)
admin.site.register(Profilis)
