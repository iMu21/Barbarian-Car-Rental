from django.urls import path
from . import views

app_name = 'member'

urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('verification/', views.VerificationView.as_view(), name='verification'),
    path('phone/add/', views.PhoneAddView.as_view(), name='phone_add'),
    path('phone/<int:pk>/edit/', views.PhoneEditView.as_view(), name='phone_edit'),
    path('phone/<int:pk>/delete/', views.PhoneDeleteView.as_view(), name='phone_delete'),
    path('website/add/', views.WebsiteAddView.as_view(), name='website_add'),
    path('website/<int:pk>/edit/', views.WebsiteEditView.as_view(), name='website_edit'),
    path('website/<int:pk>/delete/', views.WebsiteDeleteView.as_view(), name='website_delete'),
    path('search/', views.SearchView.as_view(), name='search'),
]
