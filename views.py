from django.shortcuts import render, redirect

from django.views.generic import TemplateView, CreateView, DetailView,UpdateView, DeleteView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.db.models import Q

from django.urls import reverse_lazy
from django.utils import timezone, dateformat

from django.contrib.auth.views import LoginView, LogoutView

from . import models, forms

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

class Register(FormView):
    template_name = 'base/register.html'
    form_class = forms.UserCreateForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(Register, self).get(*args, **kwargs)


# Create your views here.


class index(LoginRequiredMixin, ListView):
    model = models.Task
    template_name = 'base/index.html'
    context_object_name = 'list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = models.Task.objects.filter(user=self.request.user)
        context['count'] = models.Task.objects.filter(user=self.request.user, complete=False).count()

        search_input = self.request.GET.get('q') or ''
        if search_input:
            context['list'] = context['list'].filter(
            Q(title__icontains=search_input)|
            Q(description__icontains=search_input)
            ).distinct()

        context['search_input'] = search_input

        context['today'] = dateformat.format(timezone.now(), 'Y-m-d')
        return context


class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = models.Task
    template_name = 'base/detail.html'
    context_object_name = 'task'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

class TaskCreate(LoginRequiredMixin, CreateView):
    model = models.Task
    template_name = 'base/form.html'

    form_class = forms.CreateTask
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Task
    template_name = 'base/form_update.html'

    fields = ('title', 'description', 'due','complete')
    success_url = reverse_lazy('index')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

class TaskDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Task
    template_name = 'base/delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('index')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
