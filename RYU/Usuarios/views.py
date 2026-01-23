from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from .forms import RegistroForm
from Usuarios.models import Persona, Cuenta, Rol
from EstructuraAcademica.models import PeriodoAcademico
from Resultados.models import Prueba, PruebaUsuario, Estado

@transaction.atomic
def register(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"].strip()
            correo = form.cleaned_data["correo"].strip()

            if User.objects.filter(username__iexact=username).exists():
                messages.error(request, "El usuario ya existe")
                return render(request, "auth/register.html", {"form": form})

            # Crear Persona
            persona = Persona.objects.create(
                nombres=form.cleaned_data["nombres"],
                apellidos=form.cleaned_data["apellidos"],
                correo=correo,
                cedula=form.cleaned_data["cedula"]
            )

            # Crear User
            user = User.objects.create_user(
                username=username,
                email=correo,
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["nombres"],
                last_name=form.cleaned_data["apellidos"]
            )

            # Crear Cuenta
            cuenta = Cuenta.objects.create(persona=persona, user=user)

            # Asignar PruebaUsuario
            if cuenta.rol == Rol.ASPIRANTE and cuenta.activo:
                periodo_vigente = (PeriodoAcademico.objects.filter(vigencia=True).order_by("-id").first())

                if periodo_vigente:
                    prueba = Prueba.objects.filter(periodo_academico=periodo_vigente).first()

                    if prueba:
                        try:
                            PruebaUsuario.objects.get_or_create(
                                persona_id=persona.id,
                                prueba_id=prueba.id,
                                defaults={"estado": Estado.DISPONIBLE,"fecha_realizacion": None}
                            )
                        except Exception as e:
                            print("No se pudo crear PruebaUsuario:", repr(e))

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


