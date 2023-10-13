from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from tinymce.models import HTMLField
from PIL import Image
import requests
from bs4 import BeautifulSoup
import pytz


# Create your models here.
class Birza(models.Model):
    valandos=models.TimeField()
    kaina =models.FloatField(verbose_name='Kaina',)
    rusiuota =models.IntegerField(verbose_name='Rušiuota')
    pakrovimas  = models.BinaryField(verbose_name='Pakrovimas')
    iskrovimas  = models.BinaryField(verbose_name='Iškrovimas')


    def __str__(self):
        return f"{self.valandos} {self.kaina} {self.pakrovimas} {self.iskrovimas}"



class Klientas(models.Model):
    vardas = models.CharField(verbose_name="Vardas", max_length=20)
    pavarde = models.CharField(verbose_name="Pavardė", max_length=20)
    telefonas = models.CharField(verbose_name="Telefonas", max_length=20)
    adresas = models.CharField(verbose_name="Adresas", max_length=20)
    user = models.ForeignKey(to=User, verbose_name='Vartotojas', on_delete=models.SET_NULL, null=True, blank=True)
    aprasymas=HTMLField(verbose_name='Aprašymas',max_length=1000, default='')

    def display_objektai(self):
        objektai = self.objektai.all()
        res = ', '.join(objektas.adresas for objektas in objektai)
        return res

    def __str__(self):
        return f"{self.vardas} {self.pavarde}"

    class Meta:
        verbose_name = 'Klientas'
        verbose_name_plural = 'Klientai'


class Objektas(models.Model):
    adresas = models.CharField(verbose_name="Adresas", max_length=20)
    eso_galia = models.FloatField(verbose_name="ESO galia")
    saules_galia = models.FloatField(verbose_name="Saulės galia")
    akumuliatoriaus_talpa = models.FloatField(verbose_name="Akumuliatoriaus talpa")
    elektromobilio_talpa = models.FloatField(verbose_name="Elektromobilio talpa", default=0)
    saules_inverteris = models.BinaryField(verbose_name='Saulės inverteris')
    vaizdelis= models.ImageField(verbose_name='Vaizdelis', upload_to='vaizdeliai',null=True,blank=True)
    klientas = models.ForeignKey(to='Klientas', verbose_name='Klientas', on_delete=models.CASCADE,
                                 related_name='objektai', default='')
    user = models.ForeignKey(to=User, verbose_name='Vartotojas', on_delete=models.SET_NULL, null=True)


    LOAN_STATUS = (
        ('a', '    kraunamas'),
        ('p', '    pilnai pakrautas'),
        ('t', '    tuščias'),
        ('n', '    nenaudojamas'),
    )

    status = models.CharField(verbose_name="Būsena", choices=LOAN_STATUS, default="n", max_length=1, blank=True)

    def __str__(self):
        return f"{self.adresas} {self.klientas} {self.eso_galia} {self.saules_galia}{self.akumuliatoriaus_talpa}"

    class Meta:
        verbose_name = 'Objektas'
        verbose_name_plural = 'Objektai'

#
class ObjektasReview(models.Model):
    objektas = models.ForeignKey(to="Objektas", verbose_name="Objektas", on_delete=models.SET_NULL, null=True,
                                 blank=True,
                                 related_name='reviews')
    klientas = models.ForeignKey(to="Klientas", verbose_name="Klientas", on_delete=models.SET_NULL, null=True,
                                 blank=True,
                                 related_name='reviews')
    reviewer = models.ForeignKey(to=User, verbose_name="Vartotojas", on_delete=models.SET_NULL, null=True,
                                 blank=True)

    class Meta:
        verbose_name = "Objektas"
        verbose_name_plural = 'Objektai'


class Profilis(models.Model):
    user = models.OneToOneField(to=User, verbose_name="Vartotojas", on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="profile_pics/default.png", verbose_name="Nuotrauka", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    class Meta:
        verbose_name = 'Profilis'
        verbose_name_plural = 'Profiliai'
#
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        img = Image.open(self.nuotrauka.path)
        if img.height > 200 or img.width > 200:
            img.thumbnail((200, 200))
            img.save(self.nuotrauka.path)