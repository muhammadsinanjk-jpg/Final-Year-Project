from django.db import models
from cart.models import Order
from register_for_buyer.models import RegisterForBuyer
# Create your models here.

class Payment(models.Model):
    pay_id = models.IntegerField(primary_key=True)
    # order_id = models.IntegerField()
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.CharField(max_length=45)
    # reg_id = models.IntegerField()
    reg=models.ForeignKey(RegisterForBuyer,on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'payment'


