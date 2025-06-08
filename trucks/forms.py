from django import forms
from django.core.validators import RegexValidator


class UnloadForm(forms.Form):
    def __init__(self, trucks, *args, **kwargs):
        super().__init__(*args, **kwargs)
        coord_validator = RegexValidator(
            r'^-?\d+\.?\d*\s-?\d+\.?\d*$',
            message='Введите координаты в формате "x y" (например: "12.34 56.78")'
        )

        for truck in trucks:
            field_name = f'coord_{truck.id}'
            self.fields[field_name] = forms.CharField(
                label=f"Координаты для {truck.board_number}",
                required=True,
                validators=[coord_validator],
                widget=forms.TextInput(attrs={
                    'placeholder': 'x y',
                    'class': 'coord-input'
                }))
