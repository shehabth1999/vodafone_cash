import sys,os,django,random
from django_seed import Seed
from core import settings
sys.path.append(settings.BASE_DIR) 
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'core.settings'
)
django.setup()

seeder = Seed.seeder()

# from TravelApp.models import Travel,Area,Schedule
# from DriverApp.models import Transport,Drivers
# from ClientApp.models import Clients
# from authentication.models import User


# no = 20
# trans = Transport.objects.all()
# client = Clients.objects.all()
# driver = Drivers.objects.all()

# seeder.add_entity(Clients, no)

# seeder.add_entity(Drivers, no)

# seeder.add_entity(Transport, no,{
#     "state":0,
#     "driver":random.choice(driver)
# })

# seeder.add_entity(Area, no)

# seeder.add_entity(Schedule, no,{
#     "transport":random.choice(trans)
# })

# seeder.add_entity(Travel, no,{
#     "client":random.choice(client)
# })



# inserted_pks = seeder.execute()
# print("Seeding Done")