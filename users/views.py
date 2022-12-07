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

        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('index')

        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username)

        if not user.exists():
            return render(request, 'login.html', {'error': 'Username don\'t exist.'})

        user = user[0]

        if not user.check_password(password):
            return render(request, 'login.html', {'error': 'Password isn\'t correct'})

        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect('index')


class LogoutUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logout(request)
        return render(request, 'index.html', context={'logout': 'Just logged out successfully.'})


class RegisterUser(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        password_verification = data.get('password_verification')

        validate_user = User.objects.filter(username=username)

        if validate_user.exists():
            return render(request, 'register.html', {'error': 'Username {} already in use.'.format(username)})

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
                            password=password)  # If the given credentials are valid, return a User object.
        login(request, user)  # Persist a user id and a backend in the request. This way a user doesn't
        # have to reauthenticate on every request.

        return redirect('index')
