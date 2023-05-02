from proj_maths.models import Terms, VerbsForms, Lists, RandomWords
def db_get_terms_for_table():
    terms = []
    for i, item in enumerate(Terms.objects.all()):
        terms.append([i+1, item.name, item.pos, item.definition])
    return terms
def db_write_term(new_term, new_pos, new_definition):
    term = Terms(name=new_term, pos=new_pos, definition=new_definition, termauthor="user")
    term.save()
    if new_pos.startswith('гл'):
        verb = VerbsForms(verb=new_term, fid=term)
        verb.save()
def db_get_terms_stats():
    db_terms = len(Terms.objects.filter(termauthor="db"))
    user_terms = len(Terms.objects.filter(termauthor="user"))
    terms = Terms.objects.all()
    defin_len = [len(term.definition) for term in terms]
    stats = {
            "terms_all": db_terms + user_terms,
            "terms_own": db_terms,
            "terms_added": user_terms,
            "words_avg": sum(defin_len)/len(defin_len),
            "words_max": max(defin_len),
            "words_min": min(defin_len)
    }
    return stats

def db_get_term_for_id(id):
    return Terms.objects.get(id=id)

def db_write_list(list_name, term_id):
    item = Terms.objects.get(id=term_id)
    if item.list == '' or item.list == None:
        item.list = list_name
    else:
        item.list+=','+list_name
    list_item = Lists(word=item, list_name=list_name)
    list_item.save()
    item.save()

def db_get_list(list_name):
    terms = Terms.objects.filter(list=list_name)
    terms_oflist = []
    for i, item in enumerate(terms):
        terms_oflist.append([i+1, item.name, item.definition, item.list])
    return terms_oflist

def db_get_verbs_names():
    terms = []
    for i, item in enumerate(Terms.objects.filter(pos__startswith="гл")):
        terms.append(item.name)
    return terms

def db_add_declension(verb, skls):
    term = Terms.objects.filter(name=verb)[0]
    item = VerbsForms(verb=verb, ich=skls[0], du=skls[1], er=skls[2], ihr=skls[3], wir=skls[4], sie=skls[5], fid=term)
    item.save()

def db_get_verbs():
    return Terms.objects.filter(pos__startswith="гл")

def db_verb_conjs():
    verbs = VerbsForms.objects.filter(sie__isnull=False)
    items = []
    for verb in verbs:
        item = []
        item.append(verb.verb)
        item.append(verb.fid.definition)
        item.append(verb.ich)
        item.append(verb.du)
        item.append(verb.er)
        item.append(verb.ihr)
        item.append(verb.wir)
        item.append(verb.sie)
        items.append(item)
    return items

def db_get_list_of_lists():
    lists = Lists.objects.order_by().values_list('list_name', flat=True).distinct()
    return lists

def db_get_terms_of_list_only(listname):
    terms = Lists.objects.filter(list_name=listname)
    terms_ = []
    for term in terms:
        terms_.append(term.word.name)
    return terms_

def db_check_translations(terms, translations):
    results = []
    for i in range(len(terms)):
        if translations[i] == Terms.objects.get(name=terms[i]).definition:
            results.append((True, ''))
        else:
            results.append((False, Terms.objects.get(name=terms[i]).definition))
    return results

def db_get_random_word():
    item = RandomWords.objects.order_by('?').first()
    return ((item.word, item.translation))
