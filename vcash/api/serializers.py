from rest_framework import serializers
from django.db.models import Sum
import datetime
from vcash.models import Sim,SimLog,Device,TransactionsCash
from datetime import datetime as datet

# region Sim
class SSimLog(serializers.ModelSerializer):
    class Meta:
        model = SimLog
        fields = '__all__'

class SSim(serializers.ModelSerializer):
    class Meta:
        model = Sim
        fields = '__all__'

class Gard(serializers.ModelSerializer):
    fValue  = serializers.SerializerMethodField()
    lValue  = serializers.SerializerMethodField()
    value   = serializers.SerializerMethodField()
    send    = serializers.SerializerMethodField()
    recieve = serializers.SerializerMethodField()
    device  = serializers.SerializerMethodField()
    user    = serializers.SerializerMethodField()
    differ  = serializers.SerializerMethodField()

    class Meta:
        model = Sim
        fields = [           
            "id",
            "phone",
            "number",
            "note",
            "value",
            "send",
            "recieve",
            "fValue",
            "lValue",
            "differ",
            "isused",
            "ischanged",
            "datetime",
            "device",
            "user",
        ]
        
    def get_fValue(self,sim):
        cDate = str(datetime.datetime.now().date())
        date = self.context.get("date",cDate)
        simLog = SimLog.objects.filter(dateinsert=date,isFirst=True,sim=sim)
        return simLog[0].value if len(simLog) != 0 else 0
    
    def get_lValue(self,sim):
        cDate = str(datetime.datetime.now().date())
        date = self.context.get("date",cDate)
        simLog = SimLog.objects.filter(dateinsert=date,isLast=True,sim=sim)
        return simLog[0].value if len(simLog) != 0 else 0
    
    def get_differ(self,sim):
        cDate = str(datetime.datetime.now().date())
        date = self.context.get("date",cDate)

        simLogFV = SimLog.objects.filter(dateinsert=date,isFirst=True,sim=sim)
        fValue   =  simLogFV[0].value if len(simLogFV) != 0 else 0

        simLogLF = SimLog.objects.filter(dateinsert=date,isLast=True,sim=sim)
        lValue   =  simLogLF[0].value if len(simLogLF) != 0 else 0

        valueR  = TransactionsCash.objects.filter(date = date,isSend=False,sim=sim).aggregate(Sum('value'))['value__sum']
        receive =  valueR if valueR != None else 0

        valueS = TransactionsCash.objects.filter(date = date,isSend=True,sim=sim).aggregate(Sum('value'))['value__sum']
        send   =  valueS if valueS != None else 0
        return (fValue + receive) - (send + lValue)
    
    def get_send(self,sim):
        cDate = str(datetime.datetime.now().date())
        date = self.context.get("date",cDate)
        value = TransactionsCash.objects.filter(date = date,isSend=True,sim=sim).aggregate(Sum('value'))['value__sum']
        return value if value != None else 0
    
    def get_recieve(self,sim):
        cDate = str(datetime.datetime.now().date())
        date = self.context.get("date",cDate)
        value = TransactionsCash.objects.filter(date = date,isSend=False,sim=sim).aggregate(Sum('value'))['value__sum']
        return value if value != None else 0
    
    def get_device(self, sim):
        try: return sim.device.name
        except Exception: return ""
        
    def get_value(self,sim):
        value_sim = sim.value if sim.value != None else 0
        if sim.datetime != None:
            dtime = datet.now()
            value_send = TransactionsCash.objects.filter(sim=sim,datetime__range = (sim.datetime,dtime),isSend = True).aggregate(Sum('value'))['value__sum']
            value_send = value_send if value_send != None else 0
            
            value_get = TransactionsCash.objects.filter(sim=sim,datetime__range = (sim.datetime,dtime),isSend = False).aggregate(Sum('value'))['value__sum']
            value_get = value_get if value_get != None else 0
            return (value_sim + value_get) - value_send
        else: return value_sim

    def get_user(self, sim):
        try: return sim.user.username
        except Exception: return ""

class SSimCollection(serializers.ModelSerializer):
    user    = serializers.SerializerMethodField()
    device  = serializers.SerializerMethodField()
    month   = serializers.SerializerMethodField()
    day     = serializers.SerializerMethodField()
    value   = serializers.SerializerMethodField()

    class Meta:
        model = Sim
        fields = ['id','phone','number','slot','note',"note_plus",'value','isused','ischanged','device','user','month','day']

    
    def get_value(self,sim):
        value_sim = sim.value if sim.value != None else 0
        if sim.datetime != None:
            dtime = datet.now()
            value_send = TransactionsCash.objects.filter(sim=sim,datetime__range = (sim.datetime,dtime),isSend = True).aggregate(Sum('value'))['value__sum']
            value_send = value_send if value_send != None else 0
            
            value_get = TransactionsCash.objects.filter(sim=sim,datetime__range = (sim.datetime,dtime),isSend = False).aggregate(Sum('value'))['value__sum']
            value_get = value_get if value_get != None else 0
            return (value_sim + value_get) - value_send
        else:
            return value_sim
    def get_month(self, sim):
        value = TransactionsCash.objects.filter(sim=sim,isSend=True,datetime__year=datetime.datetime.now().year,datetime__month=datetime.datetime.now().month).aggregate(Sum('value'))['value__sum']
        return value if value != None else 0
    
    def get_day(self, sim):
        """ get transactions of this sim in current day """
        value = TransactionsCash.objects.filter(sim=sim,isSend=True,date=datetime.datetime.now().date()).aggregate(Sum('value'))['value__sum']
        return value if value != None else 0
    
    def get_user(self, sim):
            try: return sim.user.username
            except Exception: return ""

    
    def get_device(self, sim):
            try:
                return sim.device.name
            except Exception:
                return ""
    
class SSimCollectionRetrieve(serializers.ModelSerializer):
    user    = serializers.SerializerMethodField()
    month   = serializers.SerializerMethodField()
    day     = serializers.SerializerMethodField()
    value   = serializers.SerializerMethodField()
    class Meta:
        model = Sim
        fields = ['id','phone','number','slot','note','note_plus','value','isused','ischanged','device','user','month','day']
    
    def get_value(self,sim):
        
        if sim.datetime != None:
            dtime = datet.now()
            
            value_send = TransactionsCash.objects.filter(sim=sim,datetime__range = (sim.datetime,dtime),isSend = True).aggregate(Sum('value'))['value__sum']
            value_send = value_send if value_send != None else 0
            
            value_get = TransactionsCash.objects.filter(sim=sim,datetime__range = (sim.datetime,dtime),isSend = False).aggregate(Sum('value'))['value__sum']
            value_get = value_get if value_get != None else 0
            simValue = sim.value if sim.value != None else 0
            return (simValue + value_get) - value_send
        else:
            return sim.value

    def get_month(self, sim):
        value = TransactionsCash.objects.filter(sim=sim,isSend=True,datetime__year=datetime.datetime.now().year,datetime__month=datetime.datetime.now().month).aggregate(Sum('value'))['value__sum']
        return value if value != None else 0
    
    def get_day(self, sim):
        """ get transactions of this sim in current day """
        value = TransactionsCash.objects.filter(sim=sim,isSend=True,date=datetime.datetime.now().date()).aggregate(Sum('value'))['value__sum']
        return value if value != None else 0
    
    def get_user(self, sim):
            try:
                username = sim.user.username
            except Exception:
                return ""
            return username
    
    def get_device(self, sim):
            try:
                username = sim.device.name
            except Exception:
                return ""
            return username
# endregion Sim

# region Device
class SDevice(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        lookup_field = "imei"

class SDeviceCollection(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_username')
    class Meta:
        model = Device
        fields = '__all__'

    def get_username(self, device):
        try: return device.user.username
        except Exception: return ""
# endregion Device
   
# region Transactions
class STransactionsCash(serializers.ModelSerializer):
    class Meta:
        model = TransactionsCash
        fields = '__all__'

class STransactionsCashCollection(serializers.ModelSerializer):
    user  = serializers.SerializerMethodField('get_username')
    device  = serializers.SerializerMethodField('get_device')
    simno  = serializers.SerializerMethodField('get_simno')
    sim     = serializers.SerializerMethodField('get_sim')
    customer  = serializers.SerializerMethodField('get_customer')
    class Meta:
        model = TransactionsCash
        fields = [
                'id',
                'device',
                'sim',
                'simno',
                'user',
                'customer',
                'value',
                'rest',
                'operationno',
                'messagedate',
                'note',
                'isSend',

                'date',
                'time',
                'datetime',
                'timestamp',

                # 'seller',
                ]
    
    
    def get_username(self, tranc):
        try: return tranc.user.username
        except Exception: return ""

    def get_device(self, tranc):
        try: return tranc.device.name
        except Exception: return ""

    def get_sim(self, tranc):
        try: return tranc.sim.phone
        except Exception: return ""
    
    def get_simno(self, tranc):
        try: return tranc.sim.number
        except Exception: return ""

    def get_customer(self,tranc):
         try: return tranc.customer.name
         except Exception: return ""
    
# endregion Transactions