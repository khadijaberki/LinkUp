from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password  # <-- important !
from authoo.models import Employe, Etudiant  # <-- importer les modèles corrects
from .models import Profile, Friend
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        date_naissance = request.POST.get('date_naissance')
        tel = request.POST.get('tel')
        password = request.POST.get('password')
        faculty = request.POST.get('faculty')

        # Création de l'utilisateur Django
        user = User.objects.create(
            username=f"{nom.lower()}.{prenom.lower()}",
            first_name=prenom,
            last_name=nom,
            password=make_password(password)  # hasher le mot de passe
        )

        if role == 'etudiant':
            cursus = request.POST.get('cursus')
            niveau = request.POST.get('niveau')
            Etudiant.objects.create(
                user=user,
                nom=nom,
                prenom=prenom,
                date_naissance=date_naissance,
                tel=tel,
                faculty=faculty,
                cursus=cursus,
                niveau=niveau
            )
        elif role == 'employe':
            office = request.POST.get('office')
            job = request.POST.get('job')
            campus = request.POST.get('campus')
            Employe.objects.create(
                user=user,
                nom=nom,
                prenom=prenom,
                date_naissance=date_naissance,
                tel=tel,
                faculty=faculty,
                office=office,
                job=job,
                campus=campus
            )

        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome')  # rediriger vers la page d'accueil
        else:
            return render(request, 'login.html', {'error': 'Nom d’utilisateur ou mot de passe incorrect.'})
    return render(request, 'login.html')


#def welcome(request):
    return render(request, 'welcome.html')
@login_required
def welcome(request):
    user = request.user
    profile_info = None

    # Vérifier si l'utilisateur est étudiant
   # try:
    #    etudiant = Etudiant.objects.get(user=user)
     #   profile_info = f"Etudiant en {etudiant.niveau} {etudiant.cursus}"
    #except etudiant.DoesNotExist:
    #    pass
    try:
      etudiant = Etudiant.objects.get(user=user)
      titre = "Étudiante" if etudiant.sexe == 'F' else "Étudiant"
      profile_info = f"{titre} en {etudiant.niveau} {etudiant.cursus}"
    except Etudiant.DoesNotExist:
      profile_info = ""

    # Vérifier si l'utilisateur est employé
    try:
        employee = Employe.objects.get(user=user)
        profile_info = f"Employé - Poste : {employee.job} - Office : {employee.office}"
    except Employe.DoesNotExist:
        pass

    context = {
        'profile_info': profile_info
    }

    return render(request, 'welcome.html', context)
@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    return render(request, 'profile.html', {
        'profile': profile
    })
@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        profile.bio = request.POST.get('bio')
        if request.FILES.get('image'):
            profile.image = request.FILES.get('image')
        profile.save()
        return redirect('profile', username=request.user.username)

    return render(request, 'edit_profile.html', {
        'profile': profile
    })
@login_required
def add_friend(request, user_id):
    to_user = get_object_or_404(User, id=user_id)

    if to_user != request.user:
        Friend.objects.get_or_create(
            from_user=request.user,
            to_user=to_user
        )

    return redirect('profile', username=to_user.username)
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
