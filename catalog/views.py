from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, SiteVisitCounter,Poll, Choice, Vote
from .forms import CommentForm
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.db import IntegrityError
from django.http import HttpResponseForbidden


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


def poll_list(request):
    polls = Poll.objects.order_by('-pub_date')
    return render(request, 'catalog/poll_list.html', {'polls': polls})

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

    return render(request, "poll_detail.html", {
        "poll": poll,
        "already_voted": already_voted,
        "just_tried_to_vote": just_tried_to_vote
    })