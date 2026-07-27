from django.db import models
from register_for_buyer.models import RegisterForBuyer

# Create your models here.
class CompalintAndReplay(models.Model):
    com_id = models.AutoField(primary_key=True)
    complaint = models.CharField(max_length=100)
    replay = models.CharField(max_length=100)
    # reg_id = models.IntegerField()
    reg=models.ForeignKey(RegisterForBuyer,on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        managed = False
        db_table = 'compalint_and_replay'
