from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from topic.models import Topics, Questions, Answers


# Create your views here.


# def get_session_key(request):
#     if not request.session.session_key:
#         request.session.cycle_key()
#     return request.session.session_key


def topic(request, topic_id, question_id):
    topic = get_object_or_404(Topics, id=topic_id)
    questions = Questions.objects.filter(topic=topic)
    if not len(questions):
        raise Http404()
    paginator = Paginator(questions, 1)  # По 3 статьи на каждой странице.
    page = request.GET.get('page')

    if request.POST:
        print(request.POST.getlist('checkbox', None))
        try:
            page = str(int(page) + 1)
        except ValueError:
            pass
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

    return render(request, 'landing/question.html', locals())

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
