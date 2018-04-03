from django.shortcuts import render
from django.views.generic import ListView, TemplateView, View

#my imports

from .models import Thread

# Create your views here.

# class ForumView(TemplateView):
#     template_name='forum/index.html'

# # metodo de criação da view
# indexForum = ForumView.as_view()

class ForumView(ListView):
    model = Thread
    paginate_by = 3

    template_name = 'forum/index.html'

    def get_context_data(self, **kwargs):
        context = super(ForumView, self).get_context_data(**kwargs)
        context['tags'] = Thread.tags.all()
        return context

# metodo de criação da view
indexForum = ForumView.as_view()