from django.shortcuts import render
from django.core.cache import cache
from . import terms_work, terms_db


def index(request):
    w, tr = terms_db.db_get_random_word()
    context = {"w": w, "tr": tr}
    return render(request, "index.html", context=context)


def terms_list(request):
    terms = terms_db.db_get_terms_for_table()
    w, tr = terms_db.db_get_random_word()
    context = {"w": w, "tr": tr, "terms": terms}
    return render(request, "term_list.html", context=context)


def add_term(request):
    w, tr = terms_db.db_get_random_word()
    context = {"w": w, "tr": tr}
    return render(request, "term_add.html", context=context)


def send_term(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_pos = request.POST.get("pos")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        w, tr = terms_db.db_get_random_word()
        context = {"user": user_name, "w": w, "tr": tr}
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
    w, tr = terms_db.db_get_random_word()
    return render(request, "list_add.html", context={"terms": terms, "w": w, "tr": tr})

def send_list(request):
    if request.method == "POST":
        cache.clear()
        list_name = request.POST.get("listName")
        checked_items = request.POST.getlist('items')
        w, tr = terms_db.db_get_random_word()
        context = {"w": w, "tr": tr}
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
    w, tr = terms_db.db_get_random_word()
    return render(request, "verb_add.html", context={"terms": terms, "w": w, "tr": tr})

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
        w, tr = terms_db.db_get_random_word()
        context = {"w": w, "tr": tr}
        if verb in terms_db.db_get_verbs_names():
            context["success"] = True
            context["what"] = "получилось!"
            context["comment"] = "Вы успешно проспрягали глагол!"
            terms_db.db_add_declension(verb, skls)
            return render(request, "verb_request.html", context=context)
        else:
            context["success"] = False
            context["what"] = "не получилось("
            context["comment"] = "Здорово, конечно, но такого глагола в списке нет)."
            return render(request, "verb_request.html", context=context)
    else:
        return verb_add(request)

def show_verbs(request):
    verbs = terms_db.db_verb_conjs()
    w, tr = terms_db.db_get_random_word()
    return render(request, "show_verbs.html", context={"verbs":verbs, "w": w, "tr": tr})

def show_lists(request):
    lists = terms_db.db_get_list_of_lists()
    w, tr = terms_db.db_get_random_word()
    return render(request, "show_lists.html", context={"lists":lists, "w": w, "tr": tr})

def show_one_list(request):
    if request.method == 'POST':
        list_name = request.POST.get("item")
        w, tr = terms_db.db_get_random_word()
        context = {"terms":terms_db.db_get_list(list_name), "w": w, "tr": tr}
        context["listname"] = list_name
        return render(request, "show_one_list.html", context=context)
    else:
        show_lists(request)

def test_list(request):
    if request.method == 'POST':
        list_name = request.POST.get("listname")
        terms = terms_db.db_get_terms_of_list_only(list_name)
        context = {"terms":terms}
        return render(request, "test_list.html", context=context)
    else:
        show_one_list(request)

def test_result(request):
    if request.method == 'POST':
        translations = request.POST.getlist("translations")
        terms = request.POST.getlist("terms")
        res = terms_db.db_check_translations(terms, translations)
        right_answers = 0
        wrong_answers = 0
        for r in res:
            if r[0]:
                right_answers += 1
            else:
                wrong_answers += 1
        to_unzip = []
        for i in range(len(terms)):
            to_unzip.append([terms[i], translations[i], res[i][0], res[i][1]])
        context = {"items":to_unzip, "right":right_answers, "all":len(res)}
        return render(request, "test_result.html", context=context)
    else:
        test_list(request)
