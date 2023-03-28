from django.db import models

class TopLevelDomain(models.Model):
    tld = models.CharField(max_length=3)
    def __str__(self):
        return self.tld


class Country(models.Model):
    name = models.CharField(max_length=100)
    alpha2Code = models.CharField(max_length=2)
    alpha3Code = models.CharField(max_length=3)
    population = models.IntegerField()

    region = models.ForeignKey(
        "Region",
        on_delete=models.CASCADE,
        related_name="countries",
    )

    topLevelDomain = models.ManyToManyField(TopLevelDomain)
    capital = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
