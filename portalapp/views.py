from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from .models import *
from .utils import *
from .forms import TagForm, PostForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q

def example_views(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(title__icontains=search_query))
    else:

        posts = Post.objects.all()

    paginator = Paginator(posts,2)


    page_number = request.GET.get('page',1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object':page,
        'is_paginated':is_paginated,
        'prev_url':prev_url,
        'next_url':next_url,
    }


    return render(request, 'portalapp/base.html', context = context)
# Create your views here.

class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'portalapp/post_detail.html'
    #def get(self,request,slug):
    #    post = get_object_or_404(Post, slug__iexact = slug)
    #    return render(request, 'portalapp/post_detail.html', context={'post':post})

class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = 'portalapp/post_create_form.html'
    raise_exception = True

class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = TagForm
    template = 'portalapp/tag_create.html'
    raise_exception = True


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'portalapp/tag_detail.html'
    def get(self, request, slug):
        tag = Tag.objects.get(slug__iexact = slug)
        posts = tag.posts.all()
        paginator = Paginator(posts,2)
        page_number = request.GET.get('page',1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()
        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''

        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''

        context = {
            'page_object':page,
            'is_paginated':is_paginated,
            'prev_url':prev_url,
            'next_url':next_url,
            'tag':tag,
        }


        #return render(request, 'portalapp/base.html', context = context)

        return render(request, 'portalapp/tag_detail.html', context=context)

class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'portalapp/post_update_form.html'
    raise_exception = True

class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'portalapp/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True

class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'portalapp/tag_update_form.html'
    raise_exception = True

class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'portalapp/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'portalapp/tags_list.html', context={'tags': tags})


#def tag_detail(request, slug):
#    tag = Tag.objects.get(slug__iexact = slug)
#    return render(request, 'portalapp/tag_detail.html', context={'tag': tag})
