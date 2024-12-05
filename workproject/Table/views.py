from django.shortcuts import render
from main.models import Participant
from vote.models import Score
from django.http import JsonResponse


def get_all_scores(request):
    participants = Participant.objects.all()
    all_scores_data = []

    # Используем select_related для оптимизации запросов
    for participant in participants:
        scores = Score.objects.filter(participant=participant).select_related('jury')

        votes_count = scores.count()  # Количество голосов для участника
        jury_members_count = 3  # Максимальное количество жюри

        for score in scores:
            # Calculate the average score
            total_score = score.technique + score.composition + score.creativity + score.impression
            average_score = round(total_score / 4, 1)  # Среднее арифметическое с округлением до 1 знака

            all_scores_data.append({
                'jury': score.jury.username,
                'participant_number': participant.number,
                'participant_name': participant.name,
                'technique': score.technique,
                'composition': score.composition,
                'creativity': score.creativity,
                'impression': score.impression,
                'score_sum': average_score,  # Ставим среднее арифметическое
                'vote_progress': f"{votes_count}/{jury_members_count}",
            })

    return JsonResponse(all_scores_data, safe=False)


def all_participants_scores(request):
    participants = Participant.objects.all().prefetch_related('score_set')

    jury_members_count = 3  # Максимальное количество жюри
    ranked_participants = []

    for participant in participants:
        scores = participant.score_set.all()
        votes_count = scores.count()

        # Calculate the average score for each participant
        total_score = sum(score.technique + score.composition + score.creativity + score.impression for score in scores)
        average_score = round(total_score / (4 * votes_count), 1)  # Делим на общее количество оценок и округляем

        ranked_participants.append({
            'participant_number': participant.number,
            'participant_name': participant.name,
            'total_score': average_score,  # Среднее арифметическое
            'vote_progress': f"{votes_count}/{jury_members_count}",
            'fully_voted': votes_count == jury_members_count,  # Проверяем, все ли жюри проголосовали
        })

    # Сортируем рейтинг участников
    ranked_participants.sort(key=lambda x: x['total_score'], reverse=True)

    # Пронумеровываем участников
    for idx, participant in enumerate(ranked_participants, start=1):
        participant['rank'] = idx

    return render(request, 'Table/table.html', {
        'ranked_participants': ranked_participants,
        'jury_members_count': jury_members_count,
    })