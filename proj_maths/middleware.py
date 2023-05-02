from . import terms_db
class BasePageContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Добавляем контекст только для страниц, которые используют base_page.html
        if 'base_page.html' in response.content.decode('utf-8'):
            w, tr = terms_db.db_get_random_word()
            response.context_data['w'] = w
            response.context_data['tr'] = tr

        return response