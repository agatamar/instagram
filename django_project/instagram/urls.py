from django.urls import path

from django.views import generic
from instagram import views

app_name = 'instagram'
urlpatterns = [
    # path('', generic.TemplateView.as_view(template_name='twitter/index.html'),
    #      name='index'),
    path('', views.MainView.as_view(),
         name='index'),
    # path('register/',views.RegisterView.as_view(),name='register'),
    # path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('compose/',views.ComposeView.as_view(),name='compose'),
    # path('user/<int:pk>/', views.AuthorDetailView.as_view(),name='author-detail'),
    # path('tweet/<int:pk>/', views.TweetDetailView.as_view(),name='tweet-detail'),
    # path('add_message/',views.AddMessageView.as_view(),name='add_message'),
    # path('message/<int:pk>/',views.MessageDetailView.as_view(),name='message'),
    # path('messages/',views.MessageListView.as_view(),name='messages'),


]