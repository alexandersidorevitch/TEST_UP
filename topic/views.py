import time
from math import ceil

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, reverse

from topic.models import Topics, Questions, Answers

# Create your views here.


is_correct_answers = []
re_direct = False


def save(request, data, index, length):
    elements = request.POST.getlist('checkbox', None)
    if index >= len(data) or not data:
        data = [None] * length
    if elements:
        data[index] = {'type': 'checkbox', 'elements': elements}
    else:
        elements = request.POST.get('radio', None)
        if elements:
            data[index] = {'type': 'radio', 'elements': elements}
        else:
            elements = request.POST.get('text', None)
            data[index] = {'type': 'text', 'elements': elements}

    return data


def end(request, data, questions):
    count_of_right = 0
    for i, el in enumerate(data):
        if el is None:
            continue
        if el.get('type', None) == 'radio':
            if el.get('elements', None) in set(str(el.id) for el in
                                               Answers.objects.filter(question=questions[i],
                                                                      is_right=True)):
                count_of_right += 1
        elif el.get('type', None) == 'checkbox':
            if set(el.get('elements', None)) == {str(el.id) for el in
                                                 Answers.objects.filter(question=questions[i],
                                                                        is_right=True)}:
                count_of_right += 1
        elif el.get('type', None) == 'text':
            if el.get('elements', None).lower() in set(el.answer.lower() for el in
                                                       Answers.objects.filter(question=questions[i],
                                                                              is_right=True)):
                count_of_right += 1

    return count_of_right


start_time = 0


def question(request, topic_id):
    passage_of_time = 0
    global is_correct_answers, re_direct, start_time
    questions = Questions.objects.filter(topic=(get_object_or_404(Topics, id=topic_id)))
    length = len(questions)
    if not length:
        raise Http404()

    page = request.GET.get('page')

    if re_direct:
        re_direct = False
        return redirect(reverse('home'))

    paginator = Paginator(questions, 1)  # По 1 вопросу на каждой странице.
    try:
        prev_page = int(page) - 1
    except ValueError:
        prev_page = 0
    except TypeError:
        prev_page = 0
    if prev_page == 0 and not request.POST:
        start_time = time.time()
    if page is None:
        is_correct_answers = [None for _ in questions]

    count_of_correct = -1

    if request.POST:
        if '_save' in request.POST:
            save(request, is_correct_answers, prev_page, length)
            return redirect(f'/topic/{topic_id}/?page={prev_page + 2}')
        elif '_end' in request.POST:
            is_correct_answers = save(request, is_correct_answers, prev_page, length)
            count_of_correct = end(request, is_correct_answers, questions)
            passage_of_time = time.strftime('%M:%S', time.localtime(time.time() - start_time))
            start_time = 0
            re_direct = True
            mark = ceil(count_of_correct / length * 10)
            return render(request, 'landing/question.html',
                          {'prev_page': prev_page + 1, 'length': length,
                           'mark': mark, 'passage_of_time': passage_of_time, 'count_of_correct': count_of_correct})

    try:
        question = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        question = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        question = paginator.page(paginator.num_pages)

    answers = Answers.objects.filter(question=question[0]).order_by('?')

    return render(request, 'landing/question.html',
                  {'question': question, 'answers': answers, 'count_of_correct': count_of_correct,
                   'prev_page': prev_page + 1, 'length': length, })
