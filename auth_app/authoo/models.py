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
    sexe = models.CharField(
    max_length=1,
    choices=[('M', 'Masculin'), ('F', 'Féminin')],
    default='M'   # valeur par défaut
)


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
    #
    # authoo/models.py
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    tel = models.CharField(max_length=20, blank=True)
    faculty = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class Friend(models.Model):
    from_user = models.ForeignKey(
        User, related_name='friends_from', on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User, related_name='friends_to', on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}"