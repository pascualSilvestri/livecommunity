from django import forms
from apps.usuarios.models import Usuario

class ClienteForm(forms.ModelForm):
        
    class Meta:
        model = Usuario
        fields = (
            "first_name",
            "last_name",
            'email',
            'telephone',
            'fpa',
            'userTelegram',
            'userDiscord'
            )


