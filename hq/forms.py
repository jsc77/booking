from django.forms import ModelForm, TextInput
from django.forms.widgets import DateInput, DateTimeInput, RadioSelect, Select, Textarea, TimeInput
from .models import *
from django import forms
from django.forms.models import ModelChoiceField



class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=['address','mobile']

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('__all__')
        widgets = {
            'user': TextInput(attrs={'type': 'hidden', 'value':'','id': 'author_id', 'name':'name'}),
            'date': DateTimeInput(attrs={'type': 'hidden'}),
            'question1': RadioSelect(attrs={'type': ''}),
            'question2': RadioSelect(attrs={'type': ''}),
        }
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['user'].label = ""
        self.fields['question1'].label = "要介護対象ですか？"
        self.fields['question2'].label = "何人と生活していますか？"



FACILITY_CHOICES = [
    ('手すり','手すり'),
    ('車いす','車いす'),
    ('ベッド','ベッド'),
    ('杖','杖'),
    ('歩行器','歩行器'),
]

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ('__all__')
        widgets = {
            'user': TextInput(attrs={'type': 'hidden', 'value':'','id': 'user_id', 'name':'user'}),
            'location': TextInput(attrs={'type': 'text'}),
            'date': DateInput(attrs={'type':'date'}),
            'time': TimeInput(attrs={ 'type':'time'}),
            'facility': Select(choices=FACILITY_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['user'].label = ""

class BookSearchForm(ModelForm):
    user = ModelChoiceField(queryset=User.objects.all())
    
    class Meta:
        model = Book
        fields = ['user', 'date', 'facility']
        
        widgets = {
            'user': TextInput(attrs={'user':'user'}),
            'date': DateInput(attrs={'type':'date', 'name':'date'}),
            'facility': Select(choices=FACILITY_CHOICES, attrs={'name':'time'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookSearchForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['date'].required = False
        self.fields['facility'].required = False

