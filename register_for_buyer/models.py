from django.db import models

# Create your models here.
# class RegisterForBuyer(models.Model):
#     reg_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=45)
#     email = models.CharField(max_length=45)
#     phone = models.CharField(max_length=45)
#     password = models.CharField(max_length=45)
#     status = models.CharField(max_length=45)
#     photo = models.CharField(max_length=1000)


class RegisterForBuyer(models.Model):
    reg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    photo = models.CharField(max_length=1000)
    # type = models.CharField(max_length=45)   # ✅ ADD THIS

    class Meta:
        managed = False
        db_table = 'register_for_buyer'



