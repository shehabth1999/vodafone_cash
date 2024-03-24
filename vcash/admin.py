from django.contrib import admin
from vcash.models import Sim,SimLog,Device,TransactionsCash

admin.site.register(SimLog)
admin.site.register(Device)
admin.site.register(TransactionsCash)

@admin.register(Sim)
class SimM(admin.ModelAdmin):
        list_display = (
    'phone',    
    'number',   
    'note',     
    'value',    
    'isused',   
    'device',   
    'user',     
    'datetime', 
        )
        #search_fields = ('email','username','phone','account_no')
        #readonly_fields=('id', 'date_joined', 'last_login')
        filter_horizontal = ()
        list_filter = ()
        fieldsets = ()