from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from .forms import UserForm, EditUserProfileForm
from forum.models import Profile

User = get_user_model()


class UserCreateView(generic.CreateView):
    form_class = UserForm
    template_name = 'registration/register.html'
    model = User

    def get_success_url(self):
        return reverse('login')


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Profile
    form_class = EditUserProfileForm
    template_name = "edit_user_profile.html"
    success_url = reverse_lazy('home')
    success_message = "Успешно изменено"

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             "Заполните аккуратней")
        return redirect('home')

    def get_object(self):
        return self.request.slug













