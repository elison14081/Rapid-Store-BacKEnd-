from django.urls import path
from .views import NotificationListView, NotificationMarkAsReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('mark-as-read/<int:pk>/', NotificationMarkAsReadView.as_view(), name='notification-mark-as-read'),
]
