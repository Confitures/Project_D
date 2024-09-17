from django.shortcuts import render

# Create your views here.

# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import (
    ListView, DetailView, CreateView
)

from .models import Post, Category
from .filters import NewsFilter
from .forms import NewsForm


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Выводиться будут только Новости, не статьи
    queryset = Post.objects.filter(item="news")
    # Поле, которое будет использоваться для сортировки объектов
    ordering = ['time_created', ]
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'flatpages/news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsSearch(ListView):
    model = Post
    # queryset = Post.objects.filter(item="news")
    ordering = ['time_created', ]
    template_name = 'flatpages/news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/news_detail.html'
    # context_object_name = 'news_detail'
    context_object_name = 'news'


class NewsCreate(CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'flatpages/news_edit.html'

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.category = 'article'
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())


    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     # post.category = '2'
    #     # post.category = category'article'
    #     return super().form_valid(form)

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     # post.category = '2'
    #     # post.category = category'article'
    #     post.category.set('category','news')
    #     post.category.set('postcategory.category_id','1')
    #     return super().form_valid(form)


    def form_valid(self, form):
        post = form.save(commit=False)
        post.item = 'news'
        #_________________
        # category=Category.objects.filter(id='1')
        # post.category.set(category)
        # post.set(category)
        return super().form_valid(form)

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.category = 'news'
    #     return super().form_valid(form)

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.item = 'news'
    #     return super().form_valid(form)