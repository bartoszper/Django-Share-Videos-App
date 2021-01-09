from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Video
from django.contrib.auth import authenticate, login
from .forms import VideoForm, SearchForm
from django.forms import formset_factory


YOUTUBE_API_KEY = AIzaSyCDyT72BRCnDYxvxjJISkQKsj1pCml3GH0

# Create your views here.
def home(request):
    return render(request, 'main/home.html', {})

def dashboard(request):
    return render(request, 'main/dashboard.html')
class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticated(username=username, password=password1)
        login(self.request, user)
        return view

class CreateCategory(generic.CreateView):
    model = Category
    fields = ['title']
    template_name = 'main/create_category.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateCategory, self).form_valid(form)
        return redirect('home')

class DetailCategory(generic.DetailView):
    model = Category
    template_name = 'main/detail_category.html'


class UpdateCategory(generic.UpdateView):
    model = Category
    template_name = 'main/update_category.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')

class DeleteCategory(generic.DeleteView):
    model = Category
    template_name = 'main/delete_category.html'
    success_url = reverse_lazy('dashboard')

def add_video(request, pk):
    
    form = VideoForm()
    search_form = SearchForm()

    if request.method == 'POST':
        filled_form = VideoForm(request.POST)
        if filled_form.is_valid():
            
            video = Video()
            video.title = filled_form.cleaned_data['title']
            video.url = filled_form.cleaned_data['url']
            video.youtube_id = filled_form.cleaned_data['youtube_id']
            video.category = Category.objects.get(pk=pk)
            video.save()


    return render(request, 'main/add_video.html', {'form':form,'search_form': search_form})
