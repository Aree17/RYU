from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

def root_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    return redirect("login")

urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    path('', include('Usuarios.urls')),
]
