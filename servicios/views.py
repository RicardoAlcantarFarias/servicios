from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.contrib import messages
from .models import Servicio
from .forms import SolicitudServicioForm


def lista_servicios(request):
    """
    Vista para listar todos los servicios disponibles.
    """
    servicios = Servicio.objects.all()
    return render(request, 'servicios/lista_servicios.html', {'servicios': servicios})


from django.http import JsonResponse

def solicitar_servicio(request, servicio_id):
    """
    Vista para manejar solicitudes de servicios específicos.
    """
    servicio = get_object_or_404(Servicio, id=servicio_id)  # Verifica que el servicio exista
    if request.method == 'POST':
        form = SolicitudServicioForm(request.POST)
        if form.is_valid():
            try:
                correo = form.cleaned_data['correo']
                asunto = form.cleaned_data['asunto']
                mensaje = form.cleaned_data['mensaje']
                servicio_solicitado = form.cleaned_data.get('servicio', servicio)  # Asegura que el servicio esté vinculado

                # Enviar correo
                send_mail(
                    subject=f"[Solicitud de Servicio] {asunto}",
                    message=(
                        f"Solicitud de servicio: {servicio_solicitado.titulo}\n\n"
                        f"Mensaje:\n{mensaje}\n\n"
                        f"Correo de contacto: {correo}"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER],  # Reemplaza con el correo de soporte
                )
                # Devolver un JsonResponse para enviar la alerta en JavaScript
                return JsonResponse({
                    'status': 'success',
                    'message': 'Solicitud enviada. Espera a que nos contactemos contigo.'
                })
            except BadHeaderError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Se produjo un error al intentar enviar el correo. Intente nuevamente.'
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Ocurrió un error inesperado: {e}.'
                })
    else:
        form = SolicitudServicioForm(initial={'servicio': servicio})

    return render(request, 'servicios/solicitar_servicio.html', {'servicio': servicio, 'form': form})
