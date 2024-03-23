from django.db import models
from authentication.models import User

class Institution(models.Model):

    name         = models.CharField(max_length=45, blank=False, null=False,verbose_name="الإسم")
    user         = models.ForeignKey(User, on_delete = models.DO_NOTHING,verbose_name="المسئول")

    # Timestamp
    created_time = models.DateTimeField(auto_now_add=True,verbose_name="وقت الإضافة")
    update_time  = models.DateTimeField(auto_now=True,verbose_name="وقت التحديث")

    search_fields = [
        'name',
    ]

    list_filter = [
        'user',
    ]

    list_display = [
        'name',
        'user', 
        'created_time',
    ]
    def __str__(self):
        return str(self.name)
        
    class Meta:
        managed  = True
        db_table = 'institution'
        verbose_name = "المؤسسه التعليمية"
        verbose_name_plural = "المؤسسات التعليمية"
    
