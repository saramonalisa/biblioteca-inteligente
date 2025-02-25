from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario, Livro, Emprestimo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class UserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nome', 'telefone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário', 'id': 'floatingInput'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'id': 'floatingInput'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome', 'id': 'floatingInput'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone', 'id': 'floatingInput'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha', 'id': 'floatingPassword'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a senha', 'id': 'floatingPassword'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout()

class UsuarioChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = Usuario
        fields = ["username", "email", "nome", "telefone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class EmprestimoForm(forms.ModelForm):
    
    class Meta:
        model = Emprestimo
        fields = "__all__"
        widgets = {
            'usuario': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário', 'id': 'floatingInput'}),
            'livro': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Livro', 'id': 'floatingLivro'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Data', 'id': 'floatingData'}),
            'devolvido': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'flexCheckDefault'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout()
        
class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = "__all__"
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário', 'id': 'floatingInput'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'id': 'floatingInput'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome', 'id': 'floatingInput'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone', 'id': 'floatingInput'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha', 'id': 'floatingPassword'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a senha', 'id': 'floatingPassword'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout()

class classificacaoForm(forms.Form):
    classificacoes = forms.ChoiceField(choices=Livro.CLASSIFICACOES)

class GeneroForm(forms.Form):
    generos = forms.ChoiceField(choices=Livro.GENEROS)