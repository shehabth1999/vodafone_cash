from email.policy import default
from random import choices
from secrets import choice
from django.db import models
from authentication.models import User
# from customers.models import MandopInfo
from django.utils import timezone
from django.db.models.signals import pre_save,post_save
from django.core.exceptions import ValidationError
from customers.models import Customer

class Device(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    deviceid = models.CharField(unique = True,max_length=50, blank=True, null=True) 
    imei = models.CharField(unique = True,max_length=50, blank=True, null=True) 
    baddress = models.CharField(unique = True,max_length=50, blank=True, null=True) 
    user = models.ForeignKey(User,related_name="Device.Account+", on_delete = models.CASCADE,blank=True, null=True)

    def __str__(self):
        return str(self.name)
    
    def clean(self):
        super().clean()
        if self.user.max_device_number <= Device.objects.filter(user=self.user).count():
            raise ValidationError(f"Max device number must be {self.user.max_device_number} ")

    class Meta:
        managed = True
        ordering = ['-id']
        
class Sim(models.Model):
    phone       = models.CharField(unique = True,max_length=45, blank=True, null=True)
    number      = models.IntegerField(unique = True,blank=True, null=True)
    slot        = models.IntegerField(blank=True, null=True,choices=[(0,"SIM1"),(1,"SIM2"),(-1,"Unkown")])
    note        = models.TextField(blank=True, null=True)
    note_plus   = models.TextField(blank=True, null=True)
    value       = models.FloatField(blank=True, null=True)
    isused      = models.BooleanField(blank=True, null=True,default=False)  
    ischanged   = models.BooleanField(blank=True, null=True,default=False)
    device      = models.ForeignKey(Device, on_delete=models.SET_NULL,null=True)
    user        = models.ForeignKey(User,related_name="Sim.Account+", on_delete = models.CASCADE)
    datetime    = models.DateTimeField(blank=True, null=True)
    def __str__(self):return str(self.phone)

    class Meta:
        managed = True
        ordering = ['-number']

class SimLog(models.Model):
    value           = models.FloatField(blank=True, null=True)
    dateinsert      = models.DateField(blank=True, null=True) 
    timeinsert      = models.TimeField(blank=True, null=True) 
    datetimeinsert  = models.DateTimeField(blank=True, null=True)  
    dateremove      = models.DateField(blank=True, null=True) 
    timeremove      = models.TimeField(blank=True, null=True) 
    datetimeremove  = models.DateTimeField(blank=True, null=True)  
    sim             = models.ForeignKey(Sim, on_delete = models.SET_NULL,blank=True, null=True)
    isFirst         = models.BooleanField(blank=True,null=True,default=False)
    isLast          = models.BooleanField(blank=True,null=True,default=False)

    def __str__(self):return str(self.datetimeinsert)

    class Meta:
        managed = True

class TransactionsCash(models.Model):
    device      = models.ForeignKey(Device, models.SET_NULL,null=True)
    sim         = models.ForeignKey(Sim, models.SET_NULL,null=True)
    user        = models.ForeignKey(User,related_name="TransactionsCash.Account+", on_delete = models.SET_NULL,null=True)
    customer    = models.ForeignKey(Customer, on_delete=models.CASCADE)
    value       = models.FloatField()
    rest        = models.FloatField(blank=True, null=True)
    operationno = models.CharField(max_length=100, blank=True, null=True)  
    messagedate = models.CharField(max_length=100, blank=True, null=True)  
    note        = models.TextField(blank=True, null=True)
    isSend      = models.BooleanField(blank=True, null=True)

    date = models.DateField(blank=True, null=True,default=timezone.now)
    time = models.TimeField(blank=True, null=True,default=timezone.now)
    datetime = models.DateTimeField(blank=True, null=True,default=timezone.now)
    timestamp = models.BigIntegerField(blank=True, null=True)
    # seller    = models.ForeignKey(MandopInfo,related_name="TransactionsCash.MandopInfo+",on_delete = models.SET_NULL,null=True,blank=True)

    def __str__(self):return str(self.value)

    # def save(self, *args, **kwargs):
    #     if not self._state.adding and (self.creator_id != self._loaded_values['creator_id']):
    #         raise ValueError("Updating the value of creator isn't allowed")

    #     obj = TransactionsCash.objects.all().first()
    #     # print("last id",obj.id)

    #     isSameData = self.device == obj.device and \
    #     self.sim == obj.sim and \
    #     self.user == obj.user and \
    #     self.customer == obj.customer and \
    #     self.value == obj.value and \
    #     self.note == obj.note and \
    #     self.isSend == obj.isSend

    #     datetimeLastData = obj.datetime 
    #     datetimeCurrentData = self.datetime 
        
    #     if isSameData == False: 
    #         super().save(*args, **kwargs)
    #         # print(" not same "*5)
    #         return
    #     else:
    #         if  (datetimeCurrentData - datetimeLastData ).total_seconds() > 30 :
    #             # Save Action
    #             super().save(*args, **kwargs)
    #             # print((datetimeCurrentData - datetimeLastData ).total_seconds() )
    #             # print(" encrese "*5)
    #             return

    #     # print(" repeated "*5)

    class Meta:
        managed = True
        ordering = ['-datetime']


# def check_dublication_pre_save():
#     pass
# pre_save.connect(check_dublication_pre_save,sender=TransactionsCash)