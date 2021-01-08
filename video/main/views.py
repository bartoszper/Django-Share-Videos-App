from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Category


# Create your views here.
def home(request):
    return render(request, 'main/home.html', {})

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class CreateCategory(generic.CreateView):
    model = Category
    fields = ['title']
    template_name = 'main/create_category.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateCategory, self).form_valid(form)
        return redirect('home')

