from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.views.generic import ListView
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView
from .forms import *
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import redirect
from django.core.mail import send_mail

globalcnt = dict()
globalcnt["Python"] = 0

def index(request):
    globalcnt["Python"] = globalcnt["Python"] 

    mydictionary = {
        "globalcnt" : globalcnt
    }
    return render(request,'hq/index.html',context=mydictionary)

def getquery(request):
    q = request.GET['languages']
    if q in globalcnt and globalcnt[q]<100:
        # if already exist then increment the value
        globalcnt[q]=globalcnt[q]+8
        if globalcnt[q]>100:
            globalcnt[q]=100
    else:
        # first occurrence
        globalcnt[q]=100
    mydictionary = {
        "globalcnt" : globalcnt
    }
    return render(request,'hq/index.html',context=mydictionary)

def resetquery(request):
    q = request.GET['reset']
    if q in globalcnt:
        # if already exist then increment the value
        globalcnt[q]=0
    else:
        # first occurrence
        globalcnt[q]=0
    mydictionary = {
        "globalcnt" : globalcnt
    }
    return render(request,'hq/index.html',context=mydictionary)

def sortdata(request):
    global globalcnt
    globalcnt = dict(sorted(globalcnt.items(),key=lambda x:x[1],reverse=True))
    mydictionary = {
        "globalcnt" : globalcnt
    }
    return render(request,'hq/index.html',context=mydictionary)

def student_signup_view(request):
    userForm=StudentUserForm()
    studentForm=StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=StudentUserForm(request.POST)
        studentForm=StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return redirect('login')
    return render(request,'hq/signup.html',context=mydict)


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def take_exam_view(request):
    total_questions=Question.objects.all()
    
    return render(request,'hq/take_exam.html',{'total_questions':total_questions})

# class QuestionView(LoginRequiredMixin, CreateView):
#     def start_exam_view(request,pk):
#         course=Course.objects.get(id=pk)
#         return render(request,'hq/start_exam.html',{'course':course})
#     model = Question
#     form_class = forms.QuestionForm
#     template_name = 'hq/start_exam.html'
#     success_url = reverse_lazy('base')
class start_exam_view(CreateView):
    model = Question
    template_name = 'hq/start_exam.html'
    form_class = QuestionForm
    success_url = reverse_lazy('com')

class SearchResultsView(ListView):
    model = Book
    template_name = 'hq/bookDetail.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = Book.objects.filter(
                Q(user__username__icontains=query) | Q(facility__icontains=query)| Q(date__icontains=query)
            )
        else:
            object_list = Book.objects.all()
        return object_list

class SearchQuestionView(ListView):
    model = Question
    template_name = 'hq/questionDetail.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = Question.objects.filter(
                Q(user__username__icontains=query)  | Q(question1__icontains=query)| Q(question2__icontains=query)| Q(date__icontains=query)
            )
        else:
            object_list = Question.objects.all()
        return object_list

class ProfileView(View):
    def get(self,request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)
        question = Question.objects.filter(user=user).order_by('-date')
        books = Book.objects.filter(user=user).order_by('-date')
        student = Student.objects.filter(user=user)
        context ={
            'user': user,
            'books': books,
            'question': question,
            'student': student,
        }
        return render(request,'hq/profile.html', context)
class BookView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'hq/book.html'
    success_url = reverse_lazy('com')

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'hq/bookDelete.html'
    success_url = reverse_lazy('base')

def home(request):
    return render(request, 'hq/base.html', {})

def contact(request):
    if request.method == 'POST':
        message_name = request.POST['message-name']
        message_email = request.POST['message-email'] 
        message =request.POST['message']
        send_mail(message_name, message_email,message,
        ['jofew@naver.com'],
        )

        return render(request, 'hq/contact.html', {'message_name':message_name,'message_email':message_email,'message':message})
    
    else:
        return render(request, 'hq/contact.html', {})