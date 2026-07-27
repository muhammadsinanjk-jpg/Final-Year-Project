from django.db import models

# Create your models here.
class Catagory(models.Model):
    cat_id = models.AutoField(primary_key=True)
    catagory = models.CharField(max_length=45)
    image = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'catagory'
