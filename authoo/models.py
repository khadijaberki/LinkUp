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
class Etudiant(Person):
    cursus = models.CharField(max_length=100, blank=True, null=True)
    niveau = models.CharField(max_length=50, blank=True, null=True)
    sexe = models.CharField(
        max_length=1,
        choices=[('M', 'Masculin'), ('F', 'Féminin')],
        default='M'
    )

    def __str__(self):
        return f"Étudiant {self.nom}"

class Employe(Person):
    office = models.CharField(max_length=100, blank=True, null=True)
    job = models.CharField(max_length=100, blank=True, null=True)
    campus = models.CharField(max_length=100, blank=True, null=True)
    sexe = models.CharField(
        max_length=1,
        choices=[('M', 'Masculin'), ('F', 'Féminin')],
        default='M'
    )

    def __str__(self):
        return f"Employé {self.nom}"



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
    bio = models.TextField(blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True)
    faculty = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} : {self.content}"

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_friends")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_of")

    class Meta:
        unique_together = ('user', 'friend')


   