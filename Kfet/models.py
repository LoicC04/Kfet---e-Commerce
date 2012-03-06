from django.db import models

# Create your models here.
class Date(models.Model):
        models.DateTimeField('date vente')

class Menu(models.Model):
        nom = models.CharField(max_length=200)

class Information(models.Model):
        info = models.CharField(max_length=200)

class Categorie(models.Model):
        nom = models.CharField(max_length=200)

class Produit(models.Model):
        nom = models.CharField(max_length=200)
        prix = models.FloatField(blank=True, null=True)
        menu = models.ForeignKey(Menu)
        info = models.ForeignKey(Information)
        categorie = models.ForeignKey(Categorie)

class Panier(models.Model):
        date = models.ForeignKey(Date)

class Produit_Panier(models.Model):
        quantite = models.IntegerField()
        produit = models.ForeignKey(Produit)
        panier = models.ForeignKey(Panier)

class Commentaire(models.Model):
        commentaire = models.TextField()
        produit = models.ForeignKey(Produit)

class Vente(models.Model):
        produit = models.ForeignKey(Produit)
        date = models.ForeignKey(Date)
        quantite = models.IntegerField()

class Fournisseur(models.Model):
        nom = models.CharField(max_length=200)
        adresse = models.CharField(max_length=200)
        tel = models.CharField(max_length=10)
        mail = models.CharField(max_length=200)

class Personne(models.Model):
        nom = models.CharField(max_length=200)
        panier = models.ForeignKey(Panier)

class Status_Commande(models.Model):
        code = models.IntegerField()
        label = models.CharField(max_length=200)

class Reglement(models.Model):
        type = models.CharField(max_length=200)

class Commande(models.Model):
        personne = models.ForeignKey(Personne)
        type = models.ForeignKey(Status_Commande)
        reglement = models.ForeignKey(Reglement)



