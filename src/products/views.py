from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from .models import Product
# Create your views here.


def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World</h1>")
    context = {"name": "Tony"}
    return render(request, "home.html", context)


def product_detail_view(request, pk):
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise Http404
    # print(dir(request))
    # return HttpResponse(f"<h1>Product: {obj.id}</h1><p>title: {obj.title}</p><p>content: {obj.content}</p>")
    context = {"object": obj}
    return render(request, "products/product_detail.html", context)


def product_api_detail_view(request, pk, *arg, **kwargs):
    try:
        obj = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return JsonResponse({"message": "Not found"})
    return JsonResponse({"id": obj.id, "title": obj.title, "content": obj.content})


def product_list_view(request, *args, **kwargs):
    qs = Product.objects.all()
    context = {"object_list": qs}
    return render(request, "products/product_list.html", context)
