from django.db import models
from cart.models import Order
from register_for_seller.models import RegisterForSeller
# Create your models here.


class DeliveryStatus(models.Model):
    d_id = models.AutoField(primary_key=True)
    # order_id = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # sreg_id = models.IntegerField()
    sreg = models.ForeignKey(RegisterForSeller, on_delete=models.CASCADE)
    delivery_status = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'delivery_status'

