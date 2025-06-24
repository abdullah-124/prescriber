from django.db import models

# Create your models here.
class Drugs(models.Model):
    name = models.CharField(max_length=50)
    dosage = models.TextField(max_length=30)
    generic = models.TextField()
    strength = models.TextField(max_length=100)
    use_for = models.CharField(max_length=12)
    manufacturer = models.CharField(max_length=60)
    price = models.DecimalField(default=0,null=True,max_digits=8, decimal_places=2)

    class Meta:
        ordering = ['use_for',]
        pass
    def __str__(self):
        return f"{self.name}"
    