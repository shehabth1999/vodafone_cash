from django.db import models
from django.core.exceptions import ValidationError
from authentication.models import User

class Customer(models.Model):
    owner           = models.ForeignKey(User, on_delete = models.CASCADE)
    name            = models.CharField(max_length=50)
    surName         = models.CharField(max_length=50)
    customer_number = models.CharField(max_length=10, unique=True)
    phone_number    = models.CharField(max_length=50)
    rest            = models.FloatField(default=0)


    class Meta:
        unique_together = [
            ('owner', 'phone_number'),  # Unique constraint for owner and phone_number
            ('owner', 'name'),          # Unique constraint for owner and name
            ('owner', 'surName'),       # Unique constraint for owner and surName
        ]


    def clean(self):
        super().clean()
        if self.owner.max_customer_number <= Customer.objects.filter(owner=self.owner).count():
            raise ValidationError(f"Max customer number must be {self.owner.max_customer_number} ")


    def save(self, *args, **kwargs):
        if not self.customer_number:
            number_of_customer = Customer.objects.filter(owner=self.owner).count()
            # if owner id equal 1 and have 3 customer then when add another customer the customer_number will be (14) (id and forth customer)
            self.customer_number = str(self.owner_id) + str(number_of_customer + 1)
        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.name)    