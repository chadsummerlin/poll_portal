from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('index', views.index),
    path('user/create', views.create_user),
    path('user/login', views.login_user),
    path('user/logout', views.logout_user),
    path('user/<int:user_id>/yourpolls', views.your_polls),
    path('user/<int:user_id>/yourpolls/<int:poll_id>/delete', views.delete_poll),
    path('poll/form', views.poll_form),
    path('poll/create', views.create_poll),
    path('poll/<int:poll_id>/view', views.poll_view),
    path('poll/<int:poll_id>/vote/<int:answer_id>', views.vote),
    path('poll/<int:poll_id>/results', views.poll_results),
    path('<url>', views.catch_all),
    path('index/<url>', views.catch_all),
]