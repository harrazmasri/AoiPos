from django.shortcuts import redirect

class SessionAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_urls = ['/', '/register/', '/admin/']

        user_id = request.session.get('user_id')

        if not user_id and request.path not in public_urls:
            request.session.flush()
            return redirect('login')

        if user_id and request.path in ['/', '/register/']:
            return redirect('pos')

        return self.get_response(request)