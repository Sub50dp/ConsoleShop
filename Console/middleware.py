from django.utils.deprecation import MiddlewareMixin
import uuid


class AssignSessionKeyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            session_key = request.session.get('session_key')
            if not session_key:
                session_key = str(uuid.uuid4())
                request.session['session_key'] = session_key

