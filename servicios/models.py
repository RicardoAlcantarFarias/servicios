from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator, FileExtensionValidator
from django.utils.html import format_html

class Servicio(models.Model):
    """
    Modelo que representa un servicio ofrecido, incluyendo título, descripción, imagen y precio.
    """
    titulo = models.CharField(
        max_length=200,
        validators=[MaxLengthValidator(200)],
        help_text="Título del servicio (máximo 200 caracteres)."
    )
    descripcion = models.TextField(
        help_text="Descripción detallada del servicio."
    )
    imagen = models.ImageField(
        upload_to='servicios/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        help_text="Imagen representativa del servicio (formatos permitidos: JPG, JPEG, PNG)."
    )
    precio = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Precio del servicio en pesos chilenos (debe ser mayor a 0)."
    )

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['titulo']
        indexes = [
            models.Index(fields=['titulo'], name='titulo_idx'),
        ]

    def __str__(self):
        """
        Representación del modelo como una cadena.
        """
        return self.titulo

    def precio_formateado(self):
        """
        Devuelve el precio formateado con separadores de miles.
        """
        return f"${self.precio:,.0f}".replace(",", ".")  # Ejemplo: 1.000.000

    def imagen_preview(self):
        """
        Devuelve una vista previa HTML de la imagen (para el panel de administración).
        """
        if self.imagen:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', self.imagen.url)
        return "No hay imagen disponible."

    imagen_preview.short_description = "Vista Previa"
