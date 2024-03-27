from django.db import models
from django.core.exceptions import ValidationError
from authentication.models import User

class Customer(models.Model):
    user            = models.ForeignKey(User, on_delete = models.CASCADE)
    name            = models.CharField(max_length=50)
    surName         = models.CharField(max_length=50)
    customer_number = models.CharField(max_length=30, unique=True)
    phone_number    = models.CharField(max_length=50)
    address         = models.CharField(max_length=100)
    rest            = models.FloatField(default=0)

    updated_at          = models.DateTimeField(auto_now=True)
    created_at          = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('user', 'phone_number'),  # Unique constraint for owner and phone_number
            ('user', 'name'),          # Unique constraint for owner and name
            ('user', 'surName'),       # Unique constraint for owner and surName
        ]


    def clean(self):
        super().clean()
        # customer_number = Customer.objects.filter(user=self.user).count()
        # if self.user.max_customer_number <= customer_number:
        #     raise ValidationError(f"Max customer number must be {self.user.max_customer_number} ")


    def save(self, *args, **kwargs):
        if True:
            number_of_customer = Customer.objects.filter(user=self.user).count()
            # if user id equal 1 and have 3 customer then when add another customer the customer_number will be (14) (id and forth customer)
            self.customer_number = str(self.user_id) + str(number_of_customer + 1)
        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.name)    


class SupervisorLimit(models.Model):
    supervisor          = models.ForeignKey(User, on_delete= models.CASCADE, related_name='limitation',  limit_choices_to={'is_supervisor': True})
    accountant          = models.PositiveIntegerField(default=3)
    customer            = models.PositiveIntegerField(default=12)
    device              = models.PositiveIntegerField(default=3)
    sim                 = models.PositiveIntegerField(default=6)

    updated_at          = models.DateTimeField(auto_now=True)
    created_at          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)   