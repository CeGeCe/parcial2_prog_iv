from django.urls import path
from .views import DashboardView, AlumnoCreateView, enviar_pdf_alumno

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('nuevo-alumno/', AlumnoCreateView.as_view(), name='crear_alumno'),
    
    # Botón 'Enviar PDF'
    path('enviar-pdf/<int:pk>/', enviar_pdf_alumno, name='enviar_pdf'),
]