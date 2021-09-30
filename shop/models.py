from django.db import models


class SuperCategory(models.Model):
    superCategory_name=models.CharField(max_length=30,default="")

    def __str__(self):
        return self.superCategory_name

class Category(models.Model):
    category_name=models.CharField(max_length=30,default="")
    superCategory_name=models.ForeignKey(
        'SuperCategory',
        on_delete=models.SET_DEFAULT,
        default=""
        )


    def __str__(self):
        return self.category_name

class Car(models.Model):
    car_id=models.AutoField
    car_name=models.CharField(max_length=50,default="")
    car_category=models.ForeignKey(
        'Category',
        on_delete=models.SET_DEFAULT,
        default=""
        )
    car_driverRate=models.IntegerField(default=0)
    car_hourRate = models.IntegerField(default=0)
    car_deliveryRate = models.IntegerField(default=0)
    car_capacity = models.IntegerField(default=0)
    car_quantity=models.IntegerField(default=0)
    car_image=models.ImageField(upload_to='shop/images',default="")

    def __str__(self):
        return self.car_name
