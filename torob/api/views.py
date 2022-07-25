from django.shortcuts import render
from .models import Category
from .serializers import CategorySerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.paginator import Paginator

class GetCategoriesView(APIView):
    serializer_class = CategorySerializer
    lookup_url_page = 'page'
    lookup_url_size = 'size'

    def get(self, request, format=None):
        page = request.GET.get(self.lookup_url_page)
        if page == None:
            page = 1
        size = request.GET.get(self.lookup_url_size)
        if size == None:
            size = 10

        page = int(page)
        size = int(size)

        categories = Category.objects.all()
        paginator = Paginator(categories, size)

        if page not in paginator.page_range:
            return Response({"error": "Invalid page number"}, status=status.HTTP_400_BAD_REQUEST)
        paged_categories = paginator.page(page)

        next, prev = "", ""
        if page+1 in paginator.page_range:
            next = f"/category/list?page={page+1}&size={size}"
        else:
            next = None
        if page == 1:
            prev = None
        else:
            prev = f"/category/list?page={page-1}&size={size}"

        data = CategorySerializer(paged_categories, many=True).data
        response = { 
            'next': next,
            "prev": prev,
            "count": paginator.count,
            "results": data
        }
        return Response(response, status=status.HTTP_200_OK)