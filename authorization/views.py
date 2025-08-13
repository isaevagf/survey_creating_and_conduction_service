from django.shortcuts import render
from authorization.forms import UserRegistrationForm
from surveys_creating.models import Questionnaire
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save()
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'authorization/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'authorization/register.html', {'user_form': user_form})


@login_required
def dashboard(request):
    my_surveys = Questionnaire.objects.filter(author=request.user)
    return render(request, "authorization/dashboard.html", {
        "my_surveys": my_surveys
    })