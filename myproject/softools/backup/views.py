from typing import Any, Dict, Optional
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from sympy import sympify
from .models import Service, User, Word
from .forms import CustomUserCreationForm, CustomUserLoginForm
from scripts import qrcode_generator
import random
from django.db.models import Q
from difflib import get_close_matches

class RegisterView(CreateView):
    """Handle user registration."""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

class LoginView(FormView):
    """Handle user login."""
    form_class = CustomUserLoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form: Any) -> HttpResponse:
        try:
            form.validate_data(self.request)
            return super().form_valid(form)
        except ValidationError as e:
            error_message = str(e.message) if hasattr(e, 'message') else str(e)
            error_message = error_message.strip("[]'")
            messages.error(self.request, error_message)
            return self.form_invalid(form)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

class HomeView(TemplateView):
    """Display home page with services."""
    template_name = 'home.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        return context 

class CalculatorView(LoginRequiredMixin, TemplateView):
    """Handle calculator functionality."""
    template_name = 'calculator.html'
    login_url = 'login'

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        try:
            user_input = request.POST.get('expression', '')
            user_input = user_input.replace('π', 'pi').replace('÷', '/')
            calculated_result = float(sympify(user_input).evalf())
            
            if calculated_result.is_integer():
                result = int(calculated_result)
            else:
                result = '{:.6f}'.format(calculated_result).rstrip('0').rstrip('.')
                
        except Exception:
            result = "Error: Invalid input"

        return self.render_to_response({'result': result})

class DictionaryView(TemplateView):
    """Handle dictionary search functionality."""
    template_name = 'dictionary.html'

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        query = request.POST.get('query', '').strip().lower()
        context = self._search_word(query) if query else {}
        return self.render_to_response(context)

    def _search_word(self, query: str) -> Dict[str, Any]:
        try:
            exact_matches = Word.objects.filter(word__iexact=query)
            if exact_matches.exists():
                return {'word': self._format_word_results(exact_matches)}

            all_words = list(Word.objects.values_list('word', flat=True))
            similar_words = get_close_matches(query, all_words, n=3, cutoff=0.6)
            if similar_words:
                similar_matches = Word.objects.filter(word__in=similar_words)
                return {
                    'word': self._format_word_results(similar_matches),
                    'suggestion': True
                }

            partial_matches = Word.objects.filter(
                Q(word__icontains=query) | Q(description__icontains=query)
            )[:5]
            if partial_matches.exists():
                return {
                    'word': self._format_word_results(partial_matches),
                    'partial_match': True
                }

            return {'error': f'No matches found for "{query}"'}

        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}

    def _format_word_results(self, words: Any) -> list:
        return [{
            'word': word.word,
            'type': word.type,
            'description': word.description
        } for word in words]

def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'about.html')

def contact(request: HttpRequest) -> HttpResponse:
    return render(request, 'contact.html')

@login_required(login_url='login')
def qrcode_app(request: HttpRequest) -> HttpResponse:
    try:
        if request.method == 'POST':
            data = request.POST.get('data')
            fill_color = request.POST.get('fill_color')
            back_color = request.POST.get('back_color')
            
            if data:  
                image_data = qrcode_generator.generate_qr_code(data, fill_color, back_color)
                file_name = f'qrcode_{random.random()}'
                request.session['qr_data'] = {
                    'qr_image': image_data,
                    'file_name': file_name
                }
            
            if request.FILES.get('qrscan'):
                uploaded_file = request.FILES['qrscan']
                file_scan_data = qrcode_generator.scan_from_file(file_obj=uploaded_file)
                request.session['qr_data'] = {
                    'file_scan_data': file_scan_data
                }
            
            return redirect('qrcode')

        else:
            context = {}
            if 'qr_data' in request.session:
                context = request.session.pop('qr_data')
            return render(request, 'qrcode.html', context)
            
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return render(request, 'qrcode.html')

def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return redirect('/')

def services(request: HttpRequest) -> HttpResponse:
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

@login_required
def profile(request: HttpRequest) -> HttpResponse:
    user = request.user
    updates = {}
    if request.method == 'POST':
        updates = {
            'new_username': request.POST.get('username'),
            'new_email': request.POST.get('email'),
            'new_first_name': request.POST.get('first_name'),
            'new_last_name': request.POST.get('last_name'),
            'new_age': request.POST.get('age'),
            'new_gender': request.POST.get('gender'),
            'picture': request.FILES.get('pic')
        }
        
        if User.objects.filter(username=updates['new_username']).exclude(id=user.id).exists():
            messages.error(request, 'Username already exists')
            return redirect('profile')
            
        if User.objects.filter(email=updates['new_email']).exclude(id=user.id).exists():
            messages.error(request, 'Email already exists')
            return redirect('profile')
        
        if len(updates['new_first_name']) > 20 or len(updates['new_last_name']) > 20:
            messages.error(request, 'Maximum Character length 20 Char')
            return redirect('profile')
        
        if updates['new_age'] == '':
            updates['new_age'] = None
    
        user.username = updates['new_username']
        user.first_name = updates['new_first_name']
        user.last_name = updates['new_last_name']
        user.email = updates['new_email']
        user.gender = updates['new_gender']
        user.age = updates['new_age']
            
        if 'pic' in request.FILES:
            user.pic = updates['picture']
            
        try:    
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
        return redirect('profile')

    return render(request, 'profile.html', {'user': user})

@login_required(login_url='login')
def delete_account(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        try:
            user = User.objects.get(id=request.user.id)
            auth.logout(request)
            user.delete()
            messages.success(request, 'Your account has been deleted successfully')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('settings')
    return redirect('settings')

@login_required(login_url='login')
def settings_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'settings.html', {'user': request.user})


