from django.db import models
from django.contrib.auth.models import User

# CLASSE MÈRE (ABSTRAITE)
class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    tel = models.CharField(max_length=20)
    faculty = models.CharField(max_length=100)

    class Meta:
        abstract = True
class Employe(Person):
    office = models.CharField(max_length=100)
    job = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)

    def __str__(self):
        return f"Employé {self.nom}"
class Etudiant(Person):
    cursus = models.CharField(max_length=100)
    niveau = models.CharField(max_length=50)

    def __str__(self):
        return f"Étudiant {self.nom}"

from django.db import models

class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Campus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

