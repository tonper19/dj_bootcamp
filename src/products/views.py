from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, Http404
from .models import Product
from .forms import ProductModelForm
# Create your views here.


def search_view(request, *args, **kwargs):
    query = request.GET.get("q")
    qs = Product.objects.filter(title__icontains=query[0])
    print(query, qs)
    context = {"name": "Tony", "query": query}
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


def product_create_view(request, *arg, **kwargs):
    form = ProductModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # do some stuff
        obj.save()

        # data = form.cleaned_data
        # print(f"data: {data}")
        # Product.objects.create(**data)
        form = ProductModelForm()
        # return redirect("/success")
    context = {"form": form}
    return render(request, "forms.html", context)

# def product_create_view(request, *arg, **kwargs):
#     # print(f"request.POST: {request.POST}")
#     # print(f"request.GET: {request.GET}")
#     context = {}
#     if request.method == "POST":
#         post_data = request.POST or None
#         if post_data != None:
#             my_form = ProductForm(request.POST)
#             if my_form.is_valid():
#                 title_from_form = my_form.cleaned_data.get("title")
#                 Product.objects.create(title=title_from_form)
#     return render(request, "forms.html", context)

# def bad_view(request, *arg, **kwargs):
#     # http://127.0.0.1:8000/bad-view-dont-use/?new_product=True&title=Dont&content=This%20is%20not%20great%20but%20it%20works
#     my_request_data = dict(request.GET)
#     new_product = my_request_data.get("new_product")
#     print(my_request_data, new_product)
#     if new_product[0].lower() == "true":
#         print("new product")
#         Product.objects.create(
#             title=my_request_data.get("title")[0],
#             content=my_request_data.get("content")[0]
#         )
#     return HttpResponse("Dont do this")
