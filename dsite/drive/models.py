from django.db import models

# Create your models here.
class Image(models.Model):
    class Meta:
        db_table = 'mm'
    id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=255)
    title = models.CharField(max_length=255)