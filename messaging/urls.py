from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("", views.ConversationListView.as_view(), name="list"),
    path("start/<str:username>/", views.start_conversation, name="start"),
    path(
    "chat/<int:conversation_id>/",
    views.chat_view,
    name="chat"
),
    path(
        "message/<int:message_id>/edit/",
        views.edit_message,
        name="edit_message"
    ),

    path(
        "message/<int:message_id>/delete/",
        views.delete_message,
        name="delete_message"
    ),
]


