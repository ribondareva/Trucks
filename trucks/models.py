from django.contrib.gis.db import models as gis_models
from django.db import models


class TruckModel(models.Model):
    name = models.CharField(max_length=100)
    max_load = models.FloatField(help_text="Максимальная грузоподъемность, т")

    def __str__(self):
        return self.name


class Truck(models.Model):
    board_number = models.CharField(max_length=10, null=True, blank=True)
    model = models.ForeignKey(TruckModel, on_delete=models.CASCADE)
    current_load = models.FloatField(help_text="Текущий вес груза, т")
    sio2 = models.FloatField(help_text="Содержание SiO2 в %")
    fe = models.FloatField(help_text="Содержание Fe в %")
    unload_point = gis_models.PointField(null=True, blank=True)

    @property
    def overload_percent(self):
        if self.model.max_load == 0:
            return 0
        overload = self.current_load - self.model.max_load
        if overload <= 0:
            return 0
        return (overload / self.model.max_load) * 100

    def __str__(self):
        return self.board_number


class Stock(models.Model):
    name = models.CharField(max_length=100)
    volume = models.FloatField(help_text="Объем руды на складе, т")
    sio2 = models.FloatField(help_text="Содержание SiO2 в %")
    fe = models.FloatField(help_text="Содержание Fe в %")
    area = gis_models.PolygonField(help_text="WKT полигон склада")

    def __str__(self):
        return self.name
