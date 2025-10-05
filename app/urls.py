from django.urls import path
from . import views

urlpatterns = [
    path('', views.registrar_asistencia, name='registrar_asistencia'),
    path('login/descarga/', views.pagina_descarga_excel, name='pagina_descarga_excel'),
    path('login/descargar/asistencia', views.exportar_asistencia_excel, name='descargar_excel'),
    path('login/descargar/resumen/', views.exportar_resumen_excel, name='resumen_excel'),
    
]
