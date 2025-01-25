from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products')
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name
