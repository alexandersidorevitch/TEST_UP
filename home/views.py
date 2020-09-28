from django.shortcuts import render

# Create your views here.
from topic.models import Topics


def home(request):
    topics = Topics.objects.all()
    return render(request, 'landing/home.html', locals())

# def get_session_key(request):
#     if not request.session.session_key:
#         request.session.cycle_key()
#     return request.session.session_key
#
#
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
#             return home(request)
#         # Если записи сессии в БД не существует, то рендерим стартовую страницу
#         return render(request, 'home/start.html', locals())
#     # Возврат рендера домашней страницы
#     return home(request)
