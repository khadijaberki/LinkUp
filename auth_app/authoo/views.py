from django.shortcuts import render, redirect
from authoo.forms import LoginForm, StudentProfilForm

def register(request):
    if request.method == "POST":
        studentForm = StudentProfilForm(request.POST)
        if studentForm.is_valid():
            studentForm.save()
            return redirect('/login')
        else:
            return render(request, 'user_profile.html', {'studentForm': studentForm})
    else:
        studentForm = StudentProfilForm()
        return render(request, 'user_profile.html', {'studentForm': studentForm})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Ici tu peux gérer la session utilisateur si tu veux
            return redirect('/welcome')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def welcome(request):
    return render(request, 'welcome.html')

