from django.db import models

# Create your models here.
class RegisterForSeller(models.Model):
    sreg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    brand_name = models.CharField(max_length=45)
    age = models.CharField(max_length=10)
    phone = models.CharField(max_length=45)
    address = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    photo = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'register_for_seller'
