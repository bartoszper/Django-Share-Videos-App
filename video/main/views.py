from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Video
from django.contrib.auth import authenticate, login
from .forms import VideoForm, SearchForm
from django.forms import formset_factory
from django.http import Http404, JsonResponse
import urllib
import requests
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


YOUTUBE_API_KEY = 'AIzaSyCDyT72BRCnDYxvxjJISkQKsj1pCml3GH0'

# Create your views here.
def home(request):
    recent_category = Category.objects.all().order_by('-id')[:3]
    popular_category = [
        Category.objects.get(pk=1),
        Category.objects.get(pk=2),
        Category.objects.get(pk=3),
    ]   

    return render(request, 'main/home.html', {'recent_category': recent_category,'popular_category':popular_category})

@login_required
def dashboard(request):
    category = Category.objects.filter(user=request.user)
    return render(request, 'main/dashboard.html',{'category':category})


@login_required
def video_search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid(): 
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
        response = requests.get(f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={ encoded_search_term }&key={YOUTUBE_API_KEY}')
      
        return JsonResponse(response.json())
    return JsonResponse({'error': 'Not able to resposnse'})

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

class CreateCategory(LoginRequiredMixin, generic.CreateView):
    model = Category
    fields = ['title']
    template_name = 'main/create_category.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateCategory, self).form_valid(form)
        return redirect('dashboard')

class DetailCategory(generic.DetailView):
    model = Category
    template_name = 'main/detail_category.html'

   
class UpdateCategory(LoginRequiredMixin, generic.UpdateView):
    model = Category
    template_name = 'main/update_category.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        category = super(UpdateCategory, self).get_object()
        if not category.user == self.request.user:
            raise Http404
        return category

class DeleteCategory(LoginRequiredMixin, generic.DeleteView):
    model = Category
    template_name = 'main/delete_category.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        category = super(DeleteCategory, self).get_object()
        if not category.user == self.request.user:
            raise Http404
        return category

class DeleteVideo(LoginRequiredMixin, generic.DeleteView):
    model = Video
    template_name = 'main/delete_video.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super(DeleteVideo, self).get_object()
        if not video.category.user == self.request.user:
            raise Http404
        return video

@login_required
def add_video(request, pk):
    
    form = VideoForm()
    search_form = SearchForm()
    category = Category.objects.get(pk=pk)
    
    if not category.user == request.user:
        raise Http404

    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = Video()
            video.category = category
            video.url = form.cleaned_data['url']
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            if video_id:
                video.youtube_id = video_id[0]
                response = requests.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={ video_id[0] }&key={YOUTUBE_API_KEY}')
                json = response.json()
                title = json['items'][0]['snippet']['title']
                video.title = title
                video.save()
                return redirect('detail_category',pk)
            else:
                errors = form._errors.setdefault('url',ErrorList())
                errors.append('Needs to be a YouTube URL')


    return render(request, 'main/add_video.html', {'form':form,'search_form': search_form, 'category': category})
