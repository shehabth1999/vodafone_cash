import random

from django.db import transaction
from django.core.management.base import BaseCommand

# from transactionApp.models import Transactions
# from transactionApp.factories import TransactionsFactory
# from authentication.models import User
# from authentication.factories import UserFactory

# values of rows
NUM_USERS = 50
NUM_TRANS = 12


# class Command(BaseCommand):
#     help = "Generates test data"
#     @transaction.atomic
#     def handle(self, *args, **kwargs):
#         self.stdout.write("Deleting old data...")
#         models = [User, Transactions]
#         for m in models:
#             m.objects.all().delete()

#         self.stdout.write("Creating new data...")
#         # Create all the users
#         people = []
#         for _ in range(NUM_USERS):
#             person = UserFactory()
#             people.append(person)

#         # Create all the transactions
#         for _ in range(NUM_TRANS):
#             user = random.choice(people)
#             thread = TransactionsFactory(user=user)
