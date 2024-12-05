from django.shortcuts import render
from main.models import Participant
from vote.models import Score
from django.http import JsonResponse
from django.db.models import Avg

def get_translation_scores(request):
    all_scores_data = []

    # Получаем все оценки, отсортированные по жюри
    scores = Score.objects.select_related('jury').order_by('jury')

    # Группируем оценки по жюри
    jury_scores = {}
    for score in scores:
        if score.jury not in jury_scores:
            jury_scores[score.jury] = []
        jury_scores[score.jury].append({
            'technique': score.technique,
            'composition': score.composition,
            'creativity': score.creativity,
            'impression': score.impression,
            'participant': score.participant.name  # Имя участника
        })

    # Формируем данные для ответа
    for jury, scores_list in jury_scores.items():
        all_scores_data.append({
            'jury': jury.username,  # Имя жюри
            'scores': scores_list
        })

    return JsonResponse(all_scores_data, safe=False)


def all_translation_scores(request):
    # Получаем все оценки, отсортированные по жюри
    scores = Score.objects.all().select_related('jury').order_by('jury')

    # Получаем уникальные жюри для отображения колонок
    juries = scores.values('jury').distinct()

    return render(request, 'translation/translation.html', {
        'scores': scores,
        'juries': juries
    })
