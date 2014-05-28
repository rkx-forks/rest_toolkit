import pytest
from webtest import TestApp
from pyramid.config import Configurator


def make_app(config):
    return TestApp(config.make_wsgi_app())


@pytest.mark.parametrize('method', ['delete', 'get', 'post', 'put'])
def test_unallowed_method_added(method):
    config = Configurator()
    config.scan('resource_only')
    app = make_app(config)
    getattr(app, method)('/', status=405)


def test_default_options_method():
    config = Configurator()
    config.scan('resource_only')
    app = make_app(config)
    response = app.options('/')
    assert response.headers['Access-Control-Allow-Methods'] == 'OPTIONS'


def test_request_add_get_view():
    config = Configurator()
    config.scan('resource_get')
    app = make_app(config)
    app.get('/')


def test_request_default_to_json_renderer():
    config = Configurator()
    config.scan('resource_get')
    app = make_app(config)
    r = app.get('/')
    assert r.content_type == 'application/json'
    assert r.json == {'message': 'hello'}


def test_request_override_renderer():
    config = Configurator()
    config.scan('resource_get_renderer')
    app = make_app(config)
    r = app.get('/')
    assert r.content_type == 'text/plain'
    assert r.body == 'hello'
