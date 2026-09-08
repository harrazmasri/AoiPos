from urllib import request

from django.shortcuts import redirect

class SessionAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_urls = ['/', '/register/', '/admin/']
        is_admin_url = request.path == '/admin' or request.path.startswith('/admin/')

        user_id = request.session.get('user_id')

        if not user_id and request.path not in public_urls and not is_admin_url:
            request.session.flush()
            return redirect('login')

        if user_id and request.path in ['/', '/register/']:
            return redirect('pos')

        return self.get_response(request)


class RoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    
    def __call__(self, request):

        urls = ['/catalogue', '/summary/']

        role = request.session.get('user_role')
        
        if role != 'admin':
            if any(request.path.startswith(prefix) for prefix in urls):
                return redirect('pos')

        return self.get_response(request)