from django.db import models
from django.contrib.auth.models import AbstractUser

class Person(AbstractUser):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=32)
    date_naissance = models.DateField(null=True, blank=True)
    tlf = models.CharField(max_length=20, blank=True)
    friends = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=True
    )
    def __str__(self):
        return self.username
class Student(models.Model):
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE
    )
    matricule = models.CharField(max_length=20)
    niveau = models.CharField(max_length=50)

    def __str__(self):
        return f"Student {self.person.username}"

class Employee(models.Model):
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE
    )
    poste = models.CharField(max_length=50)
    salaire = models.FloatField()

    def __str__(self):
        return f"Employee {self.person.username}"
class Faculty(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom
class Campus(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)

    faculties = models.ManyToManyField(Faculty)

    def __str__(self):
        return self.nom
class Cursus(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    nom = models.CharField(max_length=100)
    annee = models.IntegerField()

    def __str__(self):
        return f"{self.nom} - {self.annee}"
class Job(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )
    titre = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.titre
class Message(models.Model):
    sender = models.ForeignKey(
        Person,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        Person,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.sender} à {self.receiver}"
