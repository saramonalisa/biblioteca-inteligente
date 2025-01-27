from django import forms
from django.core.exceptions import ValidationError
from .models import User, Perfil, Livro, Emprestimo
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import BaseUserCreationForm
from crispy_forms.layout import Layout, Row, Column, Submit

class CadastroForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-md-6'),
                Column('email', css_class='col-md-6'),
                css_class='row'
            ),
            Row(
                Column('password1', css_class='col-md-6'),
                Column('password2', css_class='col-md-6'),
                css_class='row'
            ),
            Row(
                Column(
                    Submit('submit', 'Cadastrar', css_class='col-md-12 btn btn-primary text-uppercase'),
                    css_class='col-md-12'),
                css_class='row'
            ),
        )

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
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

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout()