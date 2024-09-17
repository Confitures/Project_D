from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from django.urls import reverse_lazy
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
)

from .models import Post, Category, Subscription, User
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
        # print(f'queryset = super().get_queryset() = {queryset}')
        # # print('__________________________')
        # # print(f'queryset.category.all = {queryset.prefetch_related("post__category").all()}')
        # print('__________________________')
        # # print(f'queryset.category.all = {queryset.filter(post__category__category).all}')
        # print(f'queryset.category.all = {queryset.values("category")}')
        # print(f'queryset.category.all = {queryset.filter(id=10)}')
        # print(f'queryset.category.all = {queryset.filter().all}')

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

    def get_queryset(self):  #  Фильтр происываю
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


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'flatpages/news_edit.html'


    def form_valid(self, form):  # устанавливаю по умолчанию post.item = 'news'.
        post = form.save(commit=False)
        post.item = 'news'
        # #_________________ НЕ РАБОТАЕТ
        # category=Category.objects.filter(id='1')
        # post.category.set(category)
        # # _________________ НЕ РАБОТАЕТ
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'flatpages/news_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'flatpages/news_delete.html'
    success_url = reverse_lazy('news')


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('article.add_post',)
    form_class = NewsForm
    model = Post
    template_name = 'flatpages/articles_edit.html'

    def form_valid(self, form):  # устанавливаю по умолчанию post.item = 'article'.
        post = form.save(commit=False)
        post.item = 'article'
        return super().form_valid(form)


class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('article.change_post',)
    form_class = NewsForm
    model = Post
    queryset = Post.objects.filter(item="article")
    template_name = 'flatpages/articles_edit.html'


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('article.delete_post',)
    model = Post
    template_name = 'flatpages/articles_delete.html'
    success_url = reverse_lazy('news')

@login_required  #  !!!
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(
                user=request.user,
                category=category,
            )
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions}
    )


class CategoryListView(ListView):  #  вебинар D 9/13
    model = Post
    # template_name = 'news/category_list.html'
    template_name = 'flatpages/category_list.html'
    # template_name = 'news/category_list.html'
    # template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'
    paginate_by = 5


    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('time_created')
        # print(f'self.category: {self.category}')
        # print(f'queryset: {queryset}')
        # print('test')
        return queryset
        # return queryset, render(self.category)
        # self.category = get_object_or_404(Subscription, id=self.kwargs['category'])
        # queryset = Post.objects.filter(category=self.category).order_by('time_created')
        # return queryset

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        # context['category'] = self.category
        # return context

        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in User.objects.filter(subscriptions__category=self.category)
        #
        # print('___________________')
        # print(f'self.request.user: {self.request.user}')
        # print(f'Subscription.objects.filter(category=self.category): {Subscription.objects.filter(category=self.category)}')
        # print(f'TEST: {User.objects.filter(subscriptions__category=self.category)}')
        # # context['is_not_subscriber'] = False
        # # context['is_not_subscriber'] = True
        context['category'] = self.category
        return context

@login_required
@csrf_protect
def subscribe(request, pk):  #  вебинар D 9/13
    user = request.user
    category = Category.objects.get(id=pk)
    # category.subscribers.add(user)
    Subscription.objects.create(
        user=request.user,
        category=category,
    )
    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})




