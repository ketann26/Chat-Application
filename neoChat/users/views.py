from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

from .forms import UserRegistrationForm
# Create your views here.

def home(request):
     
     all_users= get_user_model().objects.exclude(id=request.user.id)
     context = {
         'all_users': all_users,
     }
     return render(request,'users/home.html',context)

def register(request):
     
    if request.method=='POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Sign Up successful! You can login now.')
            return redirect('login')
        
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }

    return render(request,'users/register.html',context)
