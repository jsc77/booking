from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from hq.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', student_signup_view,name='signup'),
    path('contact/', contact, name='contact'),
    path('login/', LoginView.as_view(template_name='hq/login.html'),name='login'),
    path('logout/', LogoutView.as_view(template_name='hq/logout.html'),name='logout'),
    path('dashboard/', TemplateView.as_view(template_name="hq/exam.html"), name='dashboard'),
    path('take-exam/', take_exam_view,name='take-exam'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('qsearch/', SearchQuestionView.as_view(), name='qsearch'),
    path('start-exam/', start_exam_view.as_view(),name='start-exam'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('bookdelete/<int:pk>/', BookDeleteView.as_view(), name='bookDelete'),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name="hq/base.html"), name='base'),
    path('test/', TemplateView.as_view(template_name="hq/test.html"), name='test'),
    path('facility/', TemplateView.as_view(template_name="hq/facility.html"), name='facility'),
    path('goods/', TemplateView.as_view(template_name="hq/goodsdetail.html"), name='goods'),
    path('com/', TemplateView.as_view(template_name="hq/com.html"), name='com'),
    path('qa/', TemplateView.as_view(template_name="hq/qa.html"), name='qa'),
    path('votingapp/', index,name='index'),
    path('votingapp/getquery',getquery,name='getquery'),
    path('votingapp/resetquery',resetquery,name='resetquery'),
    path('book/', BookView.as_view(), name='book'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

