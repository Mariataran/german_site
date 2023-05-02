from proj_maths.models import Terms, VerbsForms
def db_get_terms_for_table():
    terms = []
    for i, item in enumerate(Terms.objects.all()):
        terms.append([i+1, item.name, item.pos, item.definition])
    return terms
def db_write_term(new_term, new_pos, new_definition):
    term = Terms(name=new_term, pos=new_pos, definition=new_definition, termauthor="user")
    if new_pos == 'глагол':
        verb = VerbsForms(verb=new_term, fid=term.id)
        verb.save()
    term.save()
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
    print(list_name)
    item.list = list_name
    item.save()

def db_get_list(list_name):
    terms = Terms.objects.filter(list=list_name)
    terms_oflist = []
    for i, item in enumerate(terms):
        terms_oflist.append([i+1, item.name, item.definition, item.list])
    return terms_oflist

def db_get_verbs():
    terms = []
    for i, item in enumerate(Terms.objects.filter(pos="глагол")):
        terms.append(item.name)
    return terms

def db_add_declension(verb, skls):
    term = Terms.objects.filter(name=verb)[0]
    item = VerbsForms(verb=verb, ich=skls[0], du=skls[1], er=skls[2], ihr=skls[3], wir=skls[4], sie=skls[5], fid=term)
    item.save()