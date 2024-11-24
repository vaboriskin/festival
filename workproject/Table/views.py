from django.shortcuts import render
from main.models import Participant
from vote.models import Score
from django.http import JsonResponse


def get_all_scores(request):
    participants = Participant.objects.all()
    all_scores_data = []

    for participant in participants:
        scores = Score.objects.filter(participant=participant)

        # Считаем количество голосов для участника
        votes_count = len(scores)  # Количество голосов для этого участника

        # Если у участника нет оценок, можно вручную добавить пустые значения
        if not scores:
            participant_scores = [{
                'jury': "-",
                'participant_number': participant.number,
                'participant_name': participant.name,
                'technique': "-",
                'composition': "-",
                'creativity': "-",
                'impression': "-",
                'score_sum': "",  # Сумма баллов для участника без оценок
                'vote_progress': "0/3"  # Прогресс голосования
            }]
        else:
            participant_scores = [
                {
                    'jury': score.jury.username,
                    'participant_number': participant.number,
                    'participant_name': participant.name,
                    'technique': score.technique,
                    'composition': score.composition,
                    'creativity': score.creativity,
                    'impression': score.impression,
                    'score_sum': score.technique + score.composition + score.creativity + score.impression,
                    'vote_progress': f"{votes_count}/3"  # Прогресс голосования
                }
                for score in scores
            ]

        all_scores_data.extend(participant_scores)

    return JsonResponse(all_scores_data, safe=False)





def all_participants_scores(request):
    # Получаем всех участников
    participants = Participant.objects.all()

    # Количество жюри (это фиксированное значение, если нужно, можно сделать динамическим)
    jury_members_count = 3
    all_scores = {}

    # Собираем данные для всех участников
    for participant in participants:
        scores = Score.objects.filter(participant=participant)

        # Инициализация переменных для хранения данных
        scores_data = []
        total_score = 0  # Сумма баллов для участника
        votes_count = 0  # Количество голосов

        # Обрабатываем все оценки для участника
        for score in scores:
            # Суммируем баллы по каждому критерию
            score_sum = score.technique + score.composition + score.creativity + score.impression
            total_score += score_sum  # Добавляем к общей сумме баллов

            # Добавляем данные об оценке в список
            scores_data.append({
                'jury': score.jury.username,  # Имя члена жюри
                'technique': score.technique,
                'composition': score.composition,
                'creativity': score.creativity,
                'impression': score.impression,
                'score_sum': score_sum,  # Общая сумма по оценке
            })

            votes_count += 1  # Увеличиваем количество голосов

        # Прогресс голосования для участника
        vote_progress = f"{votes_count}/{jury_members_count}"

        # Проверяем, полностью ли участник получил все голоса
        fully_voted = votes_count == jury_members_count

        # Добавляем данные о баллах и голосах участника
        all_scores[participant] = {
            'scores': scores_data,
            'total_score': total_score,
            'votes_count': votes_count,
            'vote_progress': vote_progress,
            'fully_voted': fully_voted,
        }

    # Сортировка участников по общей сумме баллов (убывает)
    sorted_participants = sorted(
        all_scores.items(),
        key=lambda x: x[1]['total_score'],
        reverse=True
    )

    # Формируем рейтинг участников
    ranked_participants = []
    for idx, (participant, data) in enumerate(sorted_participants, start=1):
        ranked_participants.append({
            'rank': idx,  # Место участника
            'participant_number': participant.number,
            'participant_name': participant.name,
            'total_score': data['total_score'],
            'vote_progress': data['vote_progress'],  # Прогресс голосов
            'fully_voted': data['fully_voted'],  # Признак, что все голоса собраны
        })

    # Передаем данные в шаблон
    return render(request, 'Table/table.html', {
        'ranked_participants': ranked_participants,
        'jury_members_count': jury_members_count,  # Передаем количество жюри для отображения
    })
