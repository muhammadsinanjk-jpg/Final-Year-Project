from django.db import models
from add_product.models import AddProduct
from register_for_buyer.models import RegisterForBuyer
# Create your models here.

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    # pro_id = models.IntegerField()
    pro=models.ForeignKey(AddProduct,on_delete=models.CASCADE)
    # reg_id = models.IntegerField()
    reg=models.ForeignKey(RegisterForBuyer,on_delete=models.CASCADE)


    class Meta:
        managed = False
        db_table = 'cart'



class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    # pro_id = models.IntegerField()
    pro = models.ForeignKey(AddProduct, on_delete=models.CASCADE)
    # reg_id = models.IntegerField()
    reg = models.ForeignKey(RegisterForBuyer, on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=100)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'order'

