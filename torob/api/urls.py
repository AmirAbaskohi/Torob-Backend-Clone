from django.urls import path
from .views import GetCategoriesView

urlpatterns = [
    path('category/list', GetCategoriesView.as_view()),
]
