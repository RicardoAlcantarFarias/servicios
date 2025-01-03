from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_servicios, name='lista_servicios'),
    path('solicitar/<int:servicio_id>/', views.solicitar_servicio, name='solicitar_servicio'),
]
