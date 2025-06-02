from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Count
from django.conf import settings
from .models import Poll, PollOption, Vote
from django.http import HttpResponseForbidden

def index(request):
    polls = Poll.objects.all()  # Получаем все голосования
    return render(request, 'lab5/index.html', {'polls': polls})

def get_client_ip(request):
    # Простой способ получения IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def poll_view(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    ip = get_client_ip(request)
    can_vote = True

    # Проверка ограничений по времени голосования с этого IP
    recent_vote = Vote.objects.filter(
        poll=poll,
        ip_address=ip,
        timestamp__gte=timezone.now() - timezone.timedelta(seconds=settings.VOTE_TIME_LIMIT_SECONDS)
    ).exists()
    if recent_vote:
        can_vote = False

    if request.method == "POST" and can_vote:
        selected_options = request.POST.getlist('options')
        if len(selected_options) > poll.max_choices:
            return HttpResponseForbidden("Превышено максимальное количество вариантов для выбора.")

        for option_id in selected_options:
            option = poll.options.filter(id=option_id).first()
            if option:
                Vote.objects.create(poll=poll, option=option, ip_address=ip)

        return redirect('lab5:poll_results', poll_id=poll.id)

    context = {
        'poll': poll,
        'can_vote': can_vote,
        'vote_minutes': settings.VOTE_TIME_LIMIT_SECONDS // 60,  # Добавляем вручную
    }

    return render(request, 'lab5/poll.html', context)

def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    options = poll.options.all()
    total_votes = Vote.objects.filter(poll=poll).count()

    votes_per_option = []
    for option in options:
        votes = Vote.objects.filter(option=option).count()
        percent = (votes / total_votes * 100) if total_votes > 0 else 0
        votes_per_option.append({
            'option_text': option.option_text,
            'votes': votes,
            'percent': round(percent, 2),
        })

    return render(request, 'lab5/results.html', {
        'poll': poll,
        'votes_per_option': votes_per_option,
        'total_votes': total_votes,
    })
