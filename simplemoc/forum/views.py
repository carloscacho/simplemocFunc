import json

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (ListView, TemplateView, View, DetailView)
from django.contrib import messages
from django.http import HttpResponse

from django.http import JsonResponse
#my imports

from .models import Thread, Replay
from .forms import ReplayForm, ThreadForm



# Create your views here.

# class ForumView(TemplateView):
#     template_name='forum/index.html'

# # metodo de criação da view
# indexForum = ForumView.as_view()

class ForumView(ListView):

    paginate_by = 3

    template_name = 'forum/index.html'

    def get_queryset(self):
        queryset = Thread.objects.all()
        order = self.request.GET.get('order', '')
        if order == 'views':
            queryset = queryset.order_by('-views')
        elif order == 'comments':
            queryset = queryset.order_by('-answers')
        tag = self.kwargs.get('tag', '')
        if tag:
            queryset = queryset.filter(tags__slug__icontains=tag)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        return context

class addThreadView(TemplateView):
    model = Thread
    template_name = 'forum/addthread.html'

    def get_context_data(self, **kwargs):
        context = super(addThreadView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        context['form'] = ThreadForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        #infomar o usuario que para responder ele deve estar logado
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Para Criar um topico é necessario estar logado')
            return redirect(self.request.path)

        
        context = {}
        form = ThreadForm(self.request.POST or None)
        
        if form.is_valid():
            topico = form.save(commit=False)
            topico.author = self.request.user
            m_tags = form.cleaned_data['tags_de_Busca']
            topico.save()
            for m_tag in m_tags:
                topico.tags.add(m_tag)
            messages.success(self.request,'O Topico foi criado com sucesso')
            context['form'] = ThreadForm()
        return redirect(self.request.path)

# cada topico 
class ThreadView(DetailView):
    model= Thread
    template_name = 'forum/thread.html'

    def get(self, request, *args, **kwargs):
        response = super(ThreadView, self).get(request, *args, **kwargs)
        if self.request.user.is_authenticated and (self.object.author != self.request.user):
            self.object.views = self.object.views + 1
            self.object.save()
        return response

    def get_context_data(self, **kwargs):
        context = super(ThreadView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        context['form'] = ReplayForm(self.request.POST or None)
        return context

    def post(self, request, *args, **kwargs):
        #infomar o usuario que para responder ele deve estar logado
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Para responder ao topico é necessario estar logado')
            return redirect(self.request.path)

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = ReplayForm(self.request.POST or None)
        
        if form.is_valid():
            replay = form.save(commit=False)
            replay.thread = self.object
            replay.author = self.request.user
            replay.save()
            messages.success(self.request,'A Sua resposta foi envida com sucesso')
            context['form'] = ReplayForm()
        return self.render_to_response(context)

#when check the correct awser 
class ReplayCorrectView(View):
    correct = True

    def get(self, request, pk):
        replay = get_object_or_404(Replay, pk=pk, author=request.user)
        replay.correct  = self.correct
        replay.save()
        message = 'Resposta correta autualizada pelo Author'
        if request.is_ajax():
            
            return JsonResponse({'success': True, 'message': message})
        else:
            messages.success(request, message)
            return redirect(replay.thread.get_absolute_url())


class ReplayIncorrectView(View):
    correct = False

    def get(self, request, pk):
        replay = get_object_or_404(Replay, pk=pk, thread__author=request.user)
        replay.correct  = self.correct
        replay.save()
        message = 'Cancelamento da Resposta correta feita pelo Author'
        if request.is_ajax():
            
            return JsonResponse({'success': True, 'message': message})
        else:
            messages.error(request, message)
            return redirect(replay.thread.get_absolute_url())

class ReplayUpView(View):
    
    def get(self, request, pk):
        replay = get_object_or_404(Replay, pk=pk, author=request.user)
        replay.replay_up  = replay.replay_up + 1
        replay.save()
        messages.success(request, 'atualização da votação  positiva da resposta')
        return redirect(replay.thread.get_absolute_url())

class ReplayDownView(View):
    
    def get(self, request, pk):
        replay = get_object_or_404(Replay, pk=pk, thread__author=request.user)
        replay.replay_down  = replay.replay_down + 1
        replay.save()
        message = 'atualização da votação negativa da resposta'
        if request.is_ajax():
            return JsonResponse({'success': True, 'message': message})
        else:
            messages.success(request, message)
            return redirect(replay.thread.get_absolute_url())

# metodo de criação da view
indexForum = ForumView.as_view()
threadForum = ThreadView.as_view()
#view para  validar a resposta correta
replayCorrect= ReplayCorrectView.as_view()
replayIncorrect = ReplayIncorrectView.as_view()
#views para votação das respostas
replayUp = ReplayUpView.as_view()
replayDown = ReplayDownView.as_view()
#add Page
addtopico = addThreadView.as_view()