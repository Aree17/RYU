from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegistroForm
from .models import Persona, Cuenta
from django.contrib.auth.models import User
from django.contrib.auth import logout

def register(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data["username"]
            correo = form.cleaned_data["correo"]

            if User.objects.filter(username=username).exists():
                messages.error(request, "El usuario ya existe")
                return redirect("register")

            persona = Persona.objects.create(
                nombres=form.cleaned_data["nombres"],
                apellidos=form.cleaned_data["apellidos"],
                correo=correo,
                cedula=form.cleaned_data["cedula"]
            )

            user = User.objects.create_user(
                username=username,
                email=correo,
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["nombres"],
                last_name=form.cleaned_data["apellidos"]
            )

            Cuenta.objects.create(
                persona=persona,
                user=user
            )

            messages.success(request, "Cuenta creada correctamente")
            return redirect("login")

    else:
        form = RegistroForm()

    return render(request, "auth/register.html", {"form": form})

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)

            return redirect("home")

        else:
            messages.error(request, "Credenciales incorrectas")

    return render(request, "auth/login.html")




def logout_view(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def home(request):
    return render(request, "auth/home.html")


