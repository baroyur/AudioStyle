from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, SiteVisitCounter, Poll, Choice, Vote, Category
from .forms import CommentForm
from django.db import IntegrityError
from hitcount.views import HitCountMixin
from hitcount.models import HitCount

def product_list(request):
    # Счётчик просмотров
    counter, created = SiteVisitCounter.objects.get_or_create(pk=1)
    hit_count = HitCount.objects.get_for_object(counter)
    HitCountMixin.hit_count(request, hit_count)

    # Фильтрация по категории
    selected_category = request.GET.get('category')
    products = Product.objects.all()

    if selected_category:
        products = products.filter(category_id=selected_category)

    categories = Category.objects.all()

    return render(request, 'catalog/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': int(selected_category) if selected_category else None,
        'visit_count': counter.count,
        'hit_count': hit_count,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    hit_count = HitCount.objects.get_for_object(product)
    HitCountMixin.hit_count(request, hit_count)

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

def poll_list(request):
    polls = Poll.objects.order_by('-pub_date')

    # Нет конкретного объекта для hitcount — передадим None или создадим фиктивный
    hit_count = None

    return render(request, 'catalog/poll_list.html', {
        'polls': polls,
        'hit_count': hit_count,
    })

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    ip_address = get_client_ip(request)
    already_voted = Vote.objects.filter(poll=poll, ip_address=ip_address).exists()
    just_tried_to_vote = False

    if request.method == "POST":
        if already_voted:
            just_tried_to_vote = True
        else:
            choice_id = request.POST.get("choice")
            try:
                choice = poll.choices.get(pk=choice_id)
                choice.votes += 1
                choice.save()
                Vote.objects.create(poll=poll, ip_address=ip_address)
                return redirect("poll_detail", poll_id=poll.id)
            except (Choice.DoesNotExist, IntegrityError):
                pass  # можно обработать ошибку

    # Здесь тоже нет конкретного объекта для hitcount, так что None
    hit_count = None

    return render(request, "poll_detail.html", {
        "poll": poll,
        "already_voted": already_voted,
        "just_tried_to_vote": just_tried_to_vote,
        "hit_count": hit_count,
    })
