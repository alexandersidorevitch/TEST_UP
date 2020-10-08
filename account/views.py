from django.urls import reverse_lazy
from django.views import generic

from account.forms import SignUpView


class SignUpView(generic.CreateView):
    form_class = SignUpView
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
