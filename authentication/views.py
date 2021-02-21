from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def index_view(request):
    return redirect('auth:login')

def signin_view(request):
    if request.method.lower() == "post":
        try:
            user = User.objects.get(email=request.POST['email'])
        except:
            return render(request, 'authentication/index.html', context={"error_message": "User With Email Does Not Exist"})
        
        if authenticate(username=user.username, password=request.POST['password']):
            login(request, user)
            return redirect('dashboard:index')
        return render(request, 'authentication/index.html', context={"error_message": "Invalid Email or Password", "email": user.email})
    return render(request, 'authentication/index.html')
