from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistroForm
import socket

# Create your views here.


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # 1. Guardamos el usuario (ESTO ES LO IMPORTANTE)
            user = form.save()
            
            # 2. Intentamos enviar el mail, pero si falla, NO rompemos nada
            try:
                # 2. Le decimos a Python: "Si tardas más de 5 segs, cancela"
                socket.setdefaulttimeout(5)

                print("Intentando enviar email...")
                send_mail(
                    '¡Bienvenido al Parcial!',
                    f'Hola {user.username}, gracias por registrarte.',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                print("Email enviado con éxito.")
            except Exception as e:
                # Si falla (Timeout, Auth, lo que sea), solo lo imprimimos en el log
                print(f"⚠️ FALLÓ EL ENVÍO DE EMAIL: {e}")
                print("Continuando con el registro sin email...")

            # 3. Logueamos y redirigimos (El usuario ni se entera del fallo)
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