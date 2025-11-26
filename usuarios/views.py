from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistroForm

# Create your views here.


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Guardar usuario
            user = form.save()
            
            # ENVIAR EMAIL DE BIENVENIDA
            send_mail(
                '¡Bienvenido al Parcial!',
                f'Hola {user.username}, gracias por registrarte en nuestra plataforma.',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            
            # Loguear y redirigir
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
        # Bootstrap para el form del login
        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')