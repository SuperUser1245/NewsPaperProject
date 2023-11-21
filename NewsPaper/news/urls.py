from django.urls import path
from .views import PostList, PostDetail, FilterPostList, NewsCreate, ArticlesCreate, PostUpdate, PostDelete


urlpatterns = [
    path('', PostList.as_view(), name='posts-list'),
    path('<int:id>', PostDetail.as_view(), name='post_detail'),
    path('search/', FilterPostList.as_view()),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('<int:id>', PostDetail.as_view()),
    path('search/', FilterPostList.as_view()),
    path('news/create/', NewsCreate.as_view()),
    path('articles/create/', ArticlesCreate.as_view()),
    path('<int:id>/edit/', PostUpdate.as_view()),
    path('<int:pk>/delete/', PostDelete.as_view()),

]

