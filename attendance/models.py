from django.db import models


class Attendance(models.Model):
    search_fields  = [
        'name',
    ]

    list_filter = [
        'user',
    ]
    list_display = [
        'name',

        'user',

        'created_time',
        'update_time',
        ]
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    isapcent = models.IntegerField(db_column='isApcent', blank=True, null=True)  
    durartion = models.TimeField(blank=True, null=True)
    students_id = models.IntegerField()
    sets = models.ForeignKey('Sets', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'attendance'
        unique_together = (('id', 'students_id', 'sets'),)

