from django.contrib import admin
from authoo.models import Faculty, Etudiant, Employe, Job, Campus  # plus Student

# Inscrire les modèles dans l'admin
admin.site.register(Faculty)
admin.site.register(Etudiant)
admin.site.register(Employe)
admin.site.register(Job)
admin.site.register(Campus)

