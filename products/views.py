import json

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.contrib import messages
from django.views.generic.edit import FormMixin, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required

from products.models import Product, ProductCategory, ProductPriceChange
from products.forms import ProductForm, ProductCustomForm
from scripts.fetch_data import store_update_price
from django.db.models import F


@login_required
def index(request):
    products_with_below_targe_price = Product.objects.filter(user=request.user).filter(target_price__isnull=False).filter(target_price__gte=F('price'))
    products_at_min_price = Product.objects.filter(user=request.user).filter(
        price__isnull=False).filter(min_price__isnull=False).filter(
        max_price__isnull=False).filter(min_price__lt=F('max_price'))
    products_with_invalid_url = Product.objects.filter(user=request.user).filter(is_url_valid=False)
    products = Product.objects.filter(user=request.user)
    other_products = products.difference(products_at_min_price).difference(products_with_below_targe_price)
    # products_search_result = ProductSearchResult.objects.all()
    # products_search_result_keywords = products_search_result.values_list('search_keyword', flat=True).distinct()
    categories = ProductCategory.objects.order_by('category')
    form = ProductForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            if form.instance.url is not None:
                response = json.loads(store_update_price(form.instance.url))
                for val in ['price', 'rating', 'reviews_count', 'ratings_count', 'availability', 'availability_message']:
                    if response.get(val) is not None:
                        setattr(form.instance, val, response.get(val))
                form.instance.is_url_valid = response.get('is_url_valid')
            form.save()
            messages.success(request, f"{form.instance.name} successfully added")
            return redirect('products:index')
    else:
        form = ProductForm
        # return HttpResponseRedirect('/')
    context = {
        # 'products' : products,
        'categories': categories,
        'form': form,
        'products_with_below_targe_price': products_with_below_targe_price,
        'products_with_invalid_url': products_with_invalid_url,
        'products_at_min_price': products_at_min_price,
        'other_products': other_products,
        # 'products_search_result': products_search_result,
        # 'products_search_result_keywords':products_search_result_keywords
    }
    return render(request, 'products/index.html', context)


class ProductsListView(ListView):
    model = Product

    # queryset = ExerciseTracker.objects.all()

    def get_queryset(self):
        # self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
        # return Book.objects.filter(publisher=self.publisher)
        self.user = self.request.user if self.request.user.is_authenticated else None
        if self.user:
            return Product.objects.filter(user=self.user)
        return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        # fetching historic data
        product = context['object']
        context['historic_data'] = ProductPriceChange.objects.filter(product=product).values_list('price', 'date')
        return context


class ProductUpdateView(UpdateView):
    model = Product
    fields = ['url', 'site', 'name', 'category', 'price', 'target_price']
    template_name_suffix = '_update_form'


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('products:index')
