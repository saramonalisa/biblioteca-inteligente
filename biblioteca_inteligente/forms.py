from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario, Livro, Emprestimo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class UserForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='col-md-6'),
                Column('email', css_class='col-md-6'),
                css_class='row'
            ),
            Row(
                Column('telefone', css_class='col-md-6'),
                Column('cidade', css_class='col-md-6'),
                css_class='row'
            ),
            Row(
                Column('mensagem', css_class='col-12'),
                css_class='row'
            ),
            Submit('submit', 'Enviar', css_class='btn btn-primary text-uppercase')
        )

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout()

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout()