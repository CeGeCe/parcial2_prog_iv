from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Alumno
from .forms import AlumnoForm
import io
from django.contrib import messages  # Mostrar mensajes de éxito
from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.conf import settings

# Create your views here.


# Dashboard: Pone los alumnos en una lista
class DashboardView(LoginRequiredMixin, ListView):
    model = Alumno
    template_name = 'alumnos/dashboard.html'
    context_object_name = 'alumnos'

    # Para que cada profesor vea SOLAMENTE sus alumnos
    # def get_queryset(self):
    #     return Alumno.objects.filter(creado_por=self.request.user)

# Crear Alumno
class AlumnoCreateView(LoginRequiredMixin, CreateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'alumnos/crear_alumno.html'
    success_url = reverse_lazy('dashboard') # Volver al dashboard tras crear

    # Truco: Asignar el usuario logueado automáticamente
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)
    

def enviar_pdf_alumno(request, pk):
    # Obtener datos del alumno
    alumno = get_object_or_404(Alumno, pk=pk)

    # Generar PDF en Memoria
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    
    # Diseño simple del PDF
    p.setFont("Helvetica-Bold", 20)
    p.drawString(100, 800, "Ficha del Alumno")
    
    p.setFont("Helvetica", 14)
    p.drawString(100, 750, f"Nombre: {alumno.nombre}")
    p.drawString(100, 730, f"Apellido: {alumno.apellido}")
    p.drawString(100, 710, f"DNI: {alumno.dni}")
    p.drawString(100, 690, f"Email: {alumno.email}")
    
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(100, 650, f"Reporte generado por: {request.user.username}")
    
    p.showPage()
    p.save()
    
    # Rebobinar el buffer (Importante)
    buffer.seek(0)
    pdf_content = buffer.getvalue()
    buffer.close()

    # Configurar el Email
    email_destinatario = request.user.email  # Se envía al docente logueado
    subject = f"Reporte PDF: {alumno.apellido}, {alumno.nombre}"
    body = "Adjunto encontrarás la ficha del alumno solicitada."
    
    email = EmailMessage(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [email_destinatario],
    )
    
    # Adjuntar el PDF
    # attach(nombre_archivo, contenido_en_bytes, tipo_mimetype)
    email.attach(f'alumno_{alumno.dni}.pdf', pdf_content, 'application/pdf')
    
    # Enviar
    email.send(fail_silently=False)

    # Feedback y Redirección
    messages.success(request, f"PDF de {alumno.nombre} enviado a tu correo.")
    return redirect('home') # O 'dashboard'