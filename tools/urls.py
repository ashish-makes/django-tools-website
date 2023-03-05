from django.urls import path
from tools import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    # path('signup', views.signup, name='signup'),
    # path('login', views.login, name='login'),
    # path('blog', views.blog, name='blog'),
    # path('post/<str:slug>', views.post, name='post'),
    # path('projects', views.projects, name='projects'),
    # path('project/<str:slug>', views.project, name='project'),
    # path('categories', views.categories, name='categories'),
    # path('category/<str:category>', views.category, name='category'),
    # path('search/', views.search, name='search'),
    # path('error', views.error, name='error'),
]