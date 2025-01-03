from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Servicio

class SolicitudServicioForm(forms.Form):
    """
    Formulario para realizar solicitudes de servicios con validaciones mejoradas.
    """
    correo = forms.EmailField(
        label="Correo de contacto",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su correo electrónico'
        }),
        help_text="Debe ser un correo válido."
    )
    asunto = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el asunto de su solicitud'
        }),
        help_text="Máximo 200 caracteres."
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Escriba su mensaje aquí...',
            'rows': 5
        }),
        help_text="Describa detalladamente su solicitud."
    )
    servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.all(),
        empty_label="Seleccione un servicio",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="Servicio",
        help_text="Seleccione el servicio al que se refiere su solicitud."
    )

    def clean_correo(self):
        """
        Validación personalizada para el campo correo.
        """
        correo = self.cleaned_data.get('correo')
        try:
            validate_email(correo)
        except ValidationError:
            raise ValidationError("Ingrese un correo electrónico válido.")
        return correo

    def clean_asunto(self):
        """
        Validación personalizada para el campo asunto.
        """
        asunto = self.cleaned_data.get('asunto')
        if len(asunto) > 200:
            raise ValidationError("El asunto no puede tener más de 200 caracteres.")
        return asunto

    def clean_mensaje(self):
        """
        Validación personalizada para el campo mensaje.
        """
        mensaje = self.cleaned_data.get('mensaje')
        if len(mensaje) < 10:
            raise ValidationError("El mensaje debe tener al menos 10 caracteres.")
        return mensaje
