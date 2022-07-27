from django.urls import path
from .views import GetCategoriesView, ProductCreateOrUpdateView

urlpatterns = [
    path('category/list', GetCategoriesView.as_view(), name="categories"),
    path('product/create-or-update', ProductCreateOrUpdateView.as_view(), name="productcreate")
]
