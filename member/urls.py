from django.urls import path
from django.conf import settings
from django.conf.urls.static import static 
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('profileEdit', views.profileEdit, name='profileEdit'),
    path('profileEdited', views.profileEdited, name='profileEdited'),

    path('signUp', views.signUp, name='signUp'),
    path('logIn', views.logIn, name='logIn'),
    path('logOut', views.logOut, name='logOut'),

    path('phoneDelete', views.phoneDelete, name='phoneDelete'),
    path('phoneEdit', views.phoneEdit, name='phoneEdit'),
    path('phoneEdited', views.phoneEdited, name='phoneEdited'),
    path('phoneAdd', views.phoneAdd, name='phoneAdd'),
    path('phoneAdded', views.phoneAdded, name='phoneAdded'),

    path('websiteDelete', views.websiteDelete, name='websiteDelete'),
    path('websiteEdit', views.websiteEdit, name='websiteEdit'),
    path('websiteEdited', views.websiteEdited, name='websiteEdited'),
    path('websiteAdd', views.websiteAdd, name='websiteAdd'),
    path('websiteAdded', views.websiteAdded, name='websiteAdded'),


    path('signUpConfirmation', views.signUpConfirmation, name='signUpConfirmation'),
    path('verificationCheck',views.verificationCheck, name='verificationCheck'),
    path('logInAttempt',views.logInAttempt, name='logInAttempt'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)