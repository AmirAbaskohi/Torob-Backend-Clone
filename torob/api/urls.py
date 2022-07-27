from django.urls import path
from .views import GetCategoriesView, ProductCreateOrUpdateView, GetProductListView, ProductRedirectView

urlpatterns = [
    path('category/list', GetCategoriesView.as_view(), name="categories"),
    path('product/create-or-update', ProductCreateOrUpdateView.as_view(), name="productcreate"),
    path('product/list', GetProductListView.as_view(), name="products"),
    path('product/redirect', ProductRedirectView.as_view(), name="redirect")
]
