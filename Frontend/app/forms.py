from django import forms

class FileForm(forms.Form):
    file = forms.FileField(label='file')

class IvaForm(forms.Form):
    fecha = forms.DateField(label="fecha")
class RangoForm(forms.Form):

    fecha1 = forms.DateField(label="fecha1")
    fecha2 = forms.DateField(label="fecha2")
    valor = forms.ComboField(label="Valor",fields=[forms.CharField(max_length=20)])