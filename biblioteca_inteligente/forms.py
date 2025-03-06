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
    usuario = forms.ModelChoiceField(queryset=Usuario.objects.all(), label="Usuário")
    livro = forms.ModelChoiceField(queryset=Livro.objects.all(), label="Livro")
    devolvido = forms.BooleanField(required=False, label="Devolvido")
    class Meta:
        model = Emprestimo
        fields = ['usuario', 'livro', 'devolvido']
                    
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
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título', 'id': 'floatingInput'}),
            'autor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Autor', 'id': 'floatingInput'}),
            'editora': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Editora', 'id': 'floatingInput'}),
            'publicacao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ano de Publicação', 'id': 'floatingInput'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISBN', 'id': 'floatingInput'}),
            'classificacao': forms.Select(attrs={'class': 'form-control', 'id': 'floatingSelect'}),
            'genero': forms.Select(attrs={'class': 'form-control', 'id': 'floatingSelect'}),
            'capa': forms.ClearableFileInput(attrs={'class': 'form-control', 'id': 'floatingInput'}),
            'sinopse': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Sinopse', 'id': 'floatingSinopse'}),
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