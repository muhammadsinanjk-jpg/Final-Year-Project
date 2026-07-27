from django.db import models
from register_for_buyer.models import RegisterForBuyer
from cart.models import Order
# Create your models here.

class FeedbackAndRating(models.Model):
    feed_id = models.AutoField(primary_key=True)
    feed_back = models.CharField(max_length=45)
    rating = models.IntegerField()
    # reg_id = models.IntegerField()
    reg=models.ForeignKey(RegisterForBuyer,on_delete=models.CASCADE)
    # order_id = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'feedback_and_rating'


