from flask import Blueprint
from flask_restful import Resource, Api, abort
from flask import request, g
from functools import wraps
from .auth_models import ApiUser
from sqlalchemy.orm.exc import NoResultFound


def token_authenticate(header_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not getattr(func, 'authenticated', True):
                return func(*args, **kwargs)

            token = request.headers.get(header_name)

            if token is None:
                abort(401)

            try:
                g.account = ApiUser.query.filter(
                    ApiUser.token == token).one()
            except NoResultFound:
                abort(401)

            return func(*args, **kwargs)
        return wrapper
    return decorator


class AuthenticatedResource(Resource):
    method_decorators = [token_authenticate('AuthenticationToken')]


class HeathcheckResource(Resource):
    url = '/health'

    def get(self):
        return {'status': 'ok',
                'message': 'I am healthy'}


class AuthenticationCheck(AuthenticatedResource):
    url = '/tokenauth'

    def post(self):
        return {'status': 'ok',
                'message': f'hello {g.account.email}'}


check_bp = Blueprint('check', __name__)
check_api = Api(check_bp)


for resource in [HeathcheckResource,
                 AuthenticationCheck]:
    check_api.add_resource(resource, resource.url)
