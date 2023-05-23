from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, password_validation

from rest_framework.response import Response


# Create your views here.
class LoginUser(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')

        return render(request, 'authentication.html')

    def post(self, request):

        if request.user.is_authenticated:
            return redirect('index')

        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username)

        if not user.exists():
            return render(request, 'authentication.html', {'error': 'Username don\'t exist.'})

        user = user[0]

        if not user.check_password(password):
            return render(request, 'authentication.html', {'error': 'Password isn\'t correct'})

        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect('index')


class LogoutUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print("here")
        logout(request)
        # return render(request, 'base.html', context={'logout': 'Just logged out successfully.'})
        return redirect('index')


class RegisterUser(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        return render(request, 'authentication.html')

    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        password_verification = data.get('password_verification')

        validate_user = User.objects.filter(username=username)

        if validate_user.exists():
            return render(request, 'authentication.html', {'error': 'Username {} already in use.'.format(username)})

        try:
            password_validation.validate_password(password)
        except Exception as err:
            return render(request, 'register.html', {'error': 'Bad request, verify body parameters.'})

        if password != password_verification:
            return render(request, 'register.html', {'error': 'Passwords don\'t match.'})

        User.objects.create(username=username)
        user = User.objects.filter(username=username)[0]
        user.set_password(password)
        user.save()

        user = authenticate(username=username,
                            password=password)
        login(request, user)

        return redirect('index')
