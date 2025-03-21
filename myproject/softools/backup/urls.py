from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('calculator/', views.CalculatorView.as_view(), name='calculator'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('settings/', views.settings_view, name='settings'),
    path('qrcode/', views.qrcode_app, name='qrcode'),
    path('dictionary/', views.DictionaryView.as_view(), name='dictionary' )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
