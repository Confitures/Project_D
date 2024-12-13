from django.urls import path
# Импортируем созданное нами представление
from .views import (
    NewsList, NewsDetail, NewsSearch,
    NewsCreate, NewsUpdate, NewsDelete,
    ArticlesCreate, ArticlesUpdate, ArticlesDelete,
    subscriptions, CategoryListView, subscribe,
)


urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('news/', NewsList.as_view()),
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view(), name='news'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/update/', ArticlesUpdate.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),  #  вебинар D 9/13
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),  # вебинар D 9/13
]
