from django.db import models
from catagory.models import Catagory
# Create your models here.


class AddProduct(models.Model):
    pro_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=45)
    image_of_product = models.CharField(max_length=500)
    stock_quantity = models.IntegerField()
    description = models.CharField(max_length=100)
    product_price = models.IntegerField()
    # cat_id = models.IntegerField()
    cat=models.ForeignKey(Catagory,on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'add_product'



