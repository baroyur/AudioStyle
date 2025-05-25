from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, SiteVisitCounter
from .forms import CommentForm
from hitcount.models import HitCount
from hitcount.views import HitCountMixin


def product_list(request):
    # Получаем объект счетчика или создаем, если нет
    counter, created = SiteVisitCounter.objects.get_or_create(pk=1)
    counter.count += 1
    counter.save()

    products = Product.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products, 'visit_count': counter.count})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Получаем или создаём объект для подсчёта просмотров товара
    hit_count = HitCount.objects.get_for_object(product)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    comments = product.comments.order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = CommentForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'comments': comments,
        'form': form,
        'hit_count': hit_count,
    })
