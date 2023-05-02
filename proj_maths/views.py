from django.shortcuts import render
from django.core.cache import cache
from . import terms_work, terms_db


def index(request):
    return render(request, "index.html")


def terms_list(request):
    terms = terms_db.db_get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})


def add_term(request):
    return render(request, "term_add.html")


def send_term(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_pos = request.POST.get("pos")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Описание должно быть не пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Термин должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            terms_db.db_write_term(new_term, new_pos, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        add_term(request)


def show_stats(request):
    stats = terms_db.db_get_terms_stats()
    return render(request, "stats.html", stats)

def add_list(request):
    terms = terms_db.db_get_terms_for_table()
    return render(request, "list_add.html", context={"terms": terms})

def send_list(request):
    if request.method == "POST":
        cache.clear()
        list_name = request.POST.get("listName")
        checked_items = request.POST.getlist('items')
        context = {}
        if len(checked_items) == 0:
            context["success"] = False
            context["comment"] = f"Ваш список {list_name} не может быть пустым."
        else:
            context["success"] = True
            context["comment"] = "Ваш список:"
            for item_id in checked_items:
                terms_db.db_write_list(list_name, item_id)
            terms = terms_db.db_get_list(list_name)
            context["terms"] = terms
        return render(request, "list_request.html", context)
    else:
        add_list(request)

def verb_add(request):
    terms = terms_db.db_get_verbs()
    return render(request, "verb_add.html", context={"terms": terms})

def choose_verb(request):
    if request.method == 'POST':
        cache.clear()
        verb = request.POST.get("verb")
        skls = []
        skls.append(request.POST.get("ich"))
        skls.append(request.POST.get("du"))
        skls.append(request.POST.get("er"))
        skls.append(request.POST.get("ihr"))
        skls.append(request.POST.get("wir"))
        skls.append(request.POST.get("sie"))
        context = {}
        if verb in terms_db.db_get_verbs():
            context["success"] = True
            context["what"] = "получилось!"
            context["comment"] = "Вы успешно склонили глагол!"
            terms_db.db_add_declension(verb, skls)
            return render(request, "verb_request.html", context=context)
        else:
            context["success"] = False
            context["what"] = "не получилось("
            context["comment"] = "Здорово, конечно, но такого глагола в списке нет)."
            return render(request, "verb_request.html", context=context)
    else:
        return verb_add(request)


