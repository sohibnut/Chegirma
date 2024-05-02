from django.urls import path
from .views import NewCommentView, ReplyCommentView
urlpatterns = [
    path('new_comment/', NewCommentView.as_view()),
    path('reply_comment/', ReplyCommentView.as_view())
]
