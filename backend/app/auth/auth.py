from flask import request, jsonify
from functools import wraps
from .utils import decode_token

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

## Auth Header
def get_token_auth_header():
    """Extract token from Authorization header."""
    token = request.headers.get('Authorization', None)
    #check data
    if not token:
        raise AuthError({
            'error': 'Authorization not found',
            'status_code': 401
        }, 401)
    else :
        #Token split
        token_parts = token.split()
    if token_parts[0].lower() != 'bearer':
        raise AuthError({
            'error': 'The authorization header is missing',
            'status_code': 401
        }, 401)
    
    elif len(token_parts) != 2 :
        raise AuthError({
            'error': 'The token is incomplete',
            'status_code': 401
        }, 401)
    else :
        return token_parts[1]

def requires_auth(allowed_roles=None):
    """
    Decorator to protect routes with allowed roles.
    allowed_roles: list of allowed roles for this route.
    """
    if allowed_roles is None:
        allowed_roles = []
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = decode_token(token)
                user_role = payload.get("role")

                if user_role not in allowed_roles:
                    raise AuthError({
                        'error': 'not allowed to access this resource.',
                        'status_code': 403
                    }, 403)
                return f(payload ,*args, **kwargs)
            except AuthError as e:
                return jsonify({
                    'success': False,
                    'error': e.error['error'],
                    'status_code': e.status_code
                }), e.status_code
            except Exception as e:
                return jsonify({  
                    'success': False,
                    'error': "Authentication failed.",
                    "details": str(e),
                    'status_code': 401
                }), 401 
        return wrapper
    return decorator