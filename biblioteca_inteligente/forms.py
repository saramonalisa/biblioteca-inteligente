from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Livro, Emprestimo, Editora
from django.core.exceptions import ValidationError
from datetime import date, timedelta

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    nome = forms.CharField(max_length=100, required=True, label='Nome Completo')
    email = forms.EmailField(required=True, label='Email')
    telefone = forms.CharField(max_length=14, required=True, label='Telefone')
    
    class Meta:
        model = User
        fields = ['username', 'nome', 'email', 'telefone', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'nome', 'telefone', 'is_active', 'is_staff']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.is_staff:
            self.fields.pop('is_staff', None)
            self.fields.pop('is_active', None)

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de usuário'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha'
        })
    )

class EditoraForm(forms.ModelForm):
    class Meta:
        model = Editora
        fields = ['editora']
        widgets = {
            'editora': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da editora'
            }),
        }

class LivroForm(forms.ModelForm):
    editora = forms.ModelMultipleChoiceField(
        queryset=Editora.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        required=False
    )
    
    quantidade = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1'
        })
    )
    
    publicacao = forms.IntegerField(
        min_value=1000,
        max_value=date.today().year + 1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1000',
            'max': str(date.today().year + 1)
        })
    )
    
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'capa', 'editora', 'isbn', 'publicacao', 
                 'classificacao', 'genero', 'sinopse', 'quantidade']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título do livro'
            }),
            'autor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Autor do livro'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ISBN (13 dígitos)'
            }),
            'classificacao': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'sinopse': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Sinopse do livro...'
            }),
            'capa': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        isbn = ''.join(c for c in isbn if c.isdigit() or c.upper() == 'X')
        
        if len(isbn) not in [10, 13]:
            raise ValidationError("ISBN deve ter 10 ou 13 dígitos.")
        
        return isbn
    
    def clean_publicacao(self):
        publicacao = self.cleaned_data.get('publicacao')
        ano_atual = date.today().year
        
        if publicacao > ano_atual + 1:
            raise ValidationError(f"Ano de publicação não pode ser maior que {ano_atual + 1}")
        
        return publicacao

class EmprestimoForm(forms.ModelForm):
    livro = forms.ModelMultipleChoiceField(
        queryset=Livro.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control select2',
            'data-placeholder': 'Selecione os livros...'
        }),
        required=True
    )
    
    data_devolucao = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': date.today().isoformat()
        }),
        required=False
    )
    
    class Meta:
        model = Emprestimo
        fields = ['usuario', 'livro', 'data_devolucao']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['livro'].queryset = Livro.objects.all()
        
        self.fields['usuario'].queryset = User.objects.filter(is_active=True)
    
    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get('usuario')
        livros = cleaned_data.get('livro')
        data_devolucao = cleaned_data.get('data_devolucao')
        
        if usuario:
            emprestimos_atrasados = Emprestimo.objects.filter(
                usuario=usuario,
                devolvido=False,
                data_devolucao__lt=date.today()
            )
            if emprestimos_atrasados.exists():
                raise ValidationError(
                    f"Usuário possui {emprestimos_atrasados.count()} empréstimo(s) atrasado(s). "
                    "Regule as pendências antes de realizar novo empréstimo."
                )
        
        if livros:
            indisponiveis = []
            for livro in livros:
                if not livro.esta_disponivel():
                    indisponiveis.append(livro.titulo)
            
            if indisponiveis:
                raise ValidationError(
                    f"Os seguintes livros não estão disponíveis: {', '.join(indisponiveis)}"
                )
        
        if not data_devolucao:
            cleaned_data['data_devolucao'] = date.today() + timedelta(days=15)
        
        return cleaned_data

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'nome', 'telefone', 'is_active', 'is_staff']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.id if self.instance else None
        
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise ValidationError("Este email já está cadastrado.")
        return email

class FiltroLivrosForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por título, autor, gênero...'
        })
    )
    
    genero = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos os gêneros')] + list(Livro.GENEROS.items()),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    classificacao = forms.ChoiceField(
        required=False,
        choices=[('', 'Todas as classificações')] + list(Livro.CLASSIFICACOES.items()),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    disponivel = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos'), ('disponivel', 'Disponíveis'), ('indisponivel', 'Indisponíveis')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )