from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, reverse

from topic.models import Topics, Questions, Answers


# Create your views here.


# def get_session_key(request):
#     if not request.session.session_key:
#         request.session.cycle_key()
#     return request.session.session_key

def topic(request, topic_id):
    print('topic')
    return render(request, 'landing/question.html', locals())


is_correct_answers = []
re_direct = False


def save(request, data, index):
    elements = request.POST.getlist('checkbox', None)
    if not elements:
        elements = request.POST.get('radio', None)
        data[index] = {'type': 'radio', 'elements': elements}
    else:
        data[index] = {'type': 'checkbox', 'elements': elements}


def end(request, data, questions):
    count_of_right = 0
    for i, el in enumerate(data):
        if el is None:
            continue
        if el.get('type', None) == 'radio':
            print(set(str(el.id) for el in
                      Answers.objects.filter(question=questions[i],
                                             is_right=True)))
            if el.get('elements', None) in set(str(el.id) for el in
                                               Answers.objects.filter(question=questions[i],
                                                                      is_right=True)):
                count_of_right += 1
        elif el.get('type', None) == 'checkbox':
            print({str(el.id) for el in
                   Answers.objects.filter(question=questions[i],
                                          is_right=True)})
            if set(el.get('elements', None)) == {str(el.id) for el in
                                                 Answers.objects.filter(question=questions[i],
                                                                        is_right=True)}:
                count_of_right += 1
    return count_of_right


def question(request, topic_id):
    global is_correct_answers, re_direct
    topic = get_object_or_404(Topics, id=topic_id)
    questions = Questions.objects.filter(topic=topic)
    length = len(questions)
    if re_direct:
        re_direct = False
        return redirect(reverse('home'))
    if not length:
        raise Http404()
    paginator = Paginator(questions, 1)  # По 3 статьи на каждой странице.
    page = request.GET.get('page')
    if page == str(length):
        is_last = True
    else:
        is_last = False
    if page is None:
        prev_page = 0
        is_correct_answers = [None for _ in questions]
    else:
        prev_page = int(page) - 1
    count_of_correct = -1
    if request.POST:

        if '_save' in request.POST:
            save(request, is_correct_answers, prev_page)
        elif '_end' in request.POST:
            count_of_correct = end(request, is_correct_answers, questions)
            re_direct = True

            #     if elements in set(str(el.id) for el in
            #                        Answers.objects.filter(question=paginator.page(str(prev_page +1))[0],
            #                                               is_right=True)):
            #         is_correct_answers[prev_page] = True
            #     else:
            #         is_correct_answers[prev_page] = False
            # else:
            #     # print(set(elements))
            #     # print({el.id for el in
            #     #                      Answers.objects.filter(question=paginator.page(page)[0], is_right=True)})
            #     if set(elements) == {str(el.id) for el in
            #                          Answers.objects.filter(question=paginator.page(str(prev_page + 1))[0],
            #                                                 is_right=True)}:
            #         is_correct_answers[prev_page] = True
            #     else:
            #         is_correct_answers[prev_page] = False
            # print(is_correct_answers)

        # except:
        #     pass
    print(is_correct_answers)
    try:
        question = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        question = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        question = paginator.page(paginator.num_pages)
    if question[0].type.type == 'OneChoice':
        is_one_choice = True
    else:
        is_one_choice = False
    answers = Answers.objects.filter(question=question[0])
    percent_of_right = count_of_correct / length * 100
    return render(request, 'landing/question.html',
                  {'question': question, 'answers': answers, 'count_of_correct': count_of_correct,
                   'is_one_choice': is_one_choice, 'is_last': is_last, 'length': length,
                   'percent_of_right': percent_of_right})

# def start(request):
#     session_key = get_session_key(request)
#     try:
#         # Проверка на существоание текущей сессии в БД
#         Users.objects.get(session=session_key)
#     except models.ObjectDoesNotExist:
#         home = UserForm(request.POST or None)
#         if request.POST and home.is_valid():
#             Users.objects.create(
#                 name=home.cleaned_data["name"],
#                 group=home.cleaned_data["group"],
#                 session=session_key,
#             ).save()
#             # Возврат рендера домашней страницы
#             return question(request)
#         # Если записи сессии в БД не существует, то рендерим стартовую страницу
#         return render(request, 'home/start.html', locals())
#     # Возврат рендера домашней страницы
#     return question(request)
