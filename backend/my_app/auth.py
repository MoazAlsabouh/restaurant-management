import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from dotenv import load_dotenv
import os

AUTH0_DOMAIN =  os.environ.get("AUTH0_DOMAIN")
ALGORITHMS =  os.environ.get("ALGORITHMS")
API_AUDIENCE =  os.environ.get("API_AUDIENCE")



class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    #get token in header 
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
        # return token
    else :
        return token_parts[1]

def check_permissions(permission, payload):
    #check permissions
    if 'permissions' not in payload: 
        raise AuthError({
            'error': 'Permissions are not included in the JWT',
            'status_code': 401
        }, 401)
    elif permission not in payload['permissions'] :
        raise AuthError({
            'error': 'Permissions not found',
            'status_code': 403
        }, 403)
        # return data in user
    else :
        return True

def verify_decode_jwt(token):
    #check jwt
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}

    #check data
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    # check key in keys jwt
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # Check the JWT and return either the payload or an error
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.PyJWKClientError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 403)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 403)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator