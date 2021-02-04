from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name="Русское название")
    title_en = models.CharField(max_length=200, verbose_name="Английское название", blank=True)
    title_jp = models.CharField(max_length=200, verbose_name="Японское название", blank=True)
    image = models.ImageField(verbose_name="Картинка покемона", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    previous_evolution = models.ForeignKey('self', verbose_name="Из кого эволюционирует", on_delete=models.SET_NULL,
                                           null=True, blank=True, related_name="evolution")

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="entities")
    lat = models.FloatField(verbose_name="Lat")
    lon = models.FloatField(verbose_name="Lon")
    appeared_at = models.DateTimeField(null=True, verbose_name="Appeared at", blank=True)
    disappeared_at = models.DateTimeField(null=True, verbose_name="Disappeared at", blank=True)
    level = models.IntegerField(null=True, verbose_name="Level", blank=True)
    health = models.IntegerField(null=True, verbose_name="Health", blank=True)
    strength = models.IntegerField(null=True, verbose_name="Strength", blank=True)
    defence = models.IntegerField(null=True, verbose_name="Defence", blank=True)
    stamina = models.IntegerField(null=True, verbose_name="Stamina", blank=True)

    def __str__(self):
        return f'{self.pokemon}, lvl: {self.level}'
