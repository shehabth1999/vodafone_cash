from django.contrib import admin
from customers.models import Customer

# Register your models here.

@admin.register(Customer)
class Customer2Admin(admin.ModelAdmin):
    search_fields = ['name', ]
    # change_list_template = 'admin/cusomer_info_list2.html'
    list_display = (
        'name',
        'phone_number',
        'address',
        'created_at',
    )
