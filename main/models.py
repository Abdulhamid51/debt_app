from django.db import models


class Client(models.Model):
    CURRENCY_CHOICES = [
        ('som', 'som'),
        ('dollar', 'dollar'),
    ]
    name = models.CharField(max_length=250)
    currency = models.CharField(max_length=250, choices=CURRENCY_CHOICES, default='som')
    debt = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

class Payment(models.Model):
    TYPE_CHOICES = [
        (1, 'pay'),
        (2, 'get_debt'),
    ]
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(choices=TYPE_CHOICES)
    summa = models.IntegerField()

    def __str__(self):
        return f"{self.date}"