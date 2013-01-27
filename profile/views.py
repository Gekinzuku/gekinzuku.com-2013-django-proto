import random, hashlib, datetime
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.forms.util import ErrorList
from django.core.mail import send_mail

from profile.models import UserProfile
from profile.forms import *

def logout_page(Request):
    """
    Log out a user and redirects them back to the main page
    """
    if Request.user.is_authenticated():
        logout(Request)
    return HttpResponseRedirect('/')

# Note, ugly as fuck. Redo this eventually
def register_page(Request):
    """
    Displays a form for a user to register with and 
    then redircts them to their new profile
    """

    if Request.method == 'POST':
        form = RegisterForm(Request.POST)
        if form.is_valid():
            errors = form._errors.setdefault("__all__", ErrorList())
            try:
                User.objects.get(username__iexact=form.cleaned_data['username'])
                errors.append(u'That username is already taken.')
            except User.DoesNotExist:
                password = form.cleaned_data['password']

                if password != form.cleaned_data['verify_password']:
                    errors.append(u'Passwords must be the same.')
                elif len(password) < 8:
                    errors.append(u'Passwords must be eight characters or longer.')
                else:
                    time = datetime.datetime.now()

                    password = make_password(password)
                    user = User(username=form.cleaned_data['username'], password=password, email=form.cleaned_data['email'])
                    user.is_active = False
                    user.save()                    

                    random.seed(time)
                    m = hashlib.sha256()
                    m.update(str(random.random()))
                    m.update(user.username)
                    m.update("aBFe6KlZ46jfM8O01FrTySjKlMqWzXcVbUio36s8Jd7fnJHD4h93hv8d2hdqWeid90")
                    m.update(user.password)

                    profile = UserProfile(user=user, activation_key=m.hexdigest(), key_expires=(datetime.datetime.today() + datetime.timedelta(2)))
                    profile.save()

                    email_subject = "Welcome to Gekinzuku! Please confirm your account."
                    email_body = "Hello %s. Welcome to Gekinzuku.\n\nPlease click this link within 48 hours to activate your account: http://66.172.33.16:8080/profile/activate/%s\n\nThanks!" % (user.username, profile.activation_key)
                    send_mail(email_subject, email_body, 'donotreply@gekinzuku.com', [user.email])

                    user.backend = 'profile.backends.CaseInsensitiveModelBackend'
                    login(Request, user)
                    return HttpResponseRedirect('/profile/')
    else:
        form = RegisterForm()

    return render_to_response('registration/register.html', {'form': form}, context_instance=RequestContext(Request))

@login_required()
def profile_activate(Request, Key):
    """
    Activates the user so they can use the website
    """
    if Request.user.userprofile.activation_key == Key and Request.user.userprofile.key_expires > datetime.datetime.today():
        Request.user.is_active = True
        Request.user.save()
        return HttpResponseRedirect('/profile/')
    raise Http404
    

@login_required()
def profile_page(Request, Username):
    """
    Displays the requested user, if None display logged in user
    """
    if Username == None:
        UserObj = UserProfile.objects.filter(user=Request.user)[0] 
    else:
        UserObj = get_object_or_404(User, username__iexact=Username)
        UserObj = UserProfile.objects.filter(user=UserObj)[0]
        
    return render_to_response('profile/profile.html', {'profile': UserObj}, context_instance=RequestContext(Request))

@login_required()
def profile_edit(Request):
    """
    Allows one to edit their profile
    """

    if Request.method == 'POST':
        form = EditProfileForm(Request.POST)
        if form.is_valid():

            return HttpResponseRedirect('/profile/')
    else:
        form = EditProfileForm()

    return render_to_response('profile/edit.html', {'form': form}, context_instance=RequestContext(Request))

@login_required()
def achievements_page(Request, Username):
    return HttpResponse("Achievements don't exist yet :(")

