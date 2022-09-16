---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# From Raw WSGI to a framework

While useful for understanding how WSGI works, the examples
shown until now are still far being called a framework.
A Python web framework usually has the following attributes:

> 1. It pre-processes the environment and yields some `request` object
>    for the programmer to work with.
>    This request is sometimes injected to the callable we program, as
>    for example in Pyramid:
>
> > ```python
> > # First view, available at http://localhost:6543/
> > @view_config(route_name='home')
> > def home(request):
> >     return Response('<body>Visit <a href="/howdy">hello</a></body>')
> >
> > # /howdy
> > @view_config(route_name='hello')
> > def hello(request):
> >     return Response('<body>Go back <a href="/">home</a></body>')
> > ```
>
> or in Django:
>
> > ```python
> > from django.http import HttpResponse
> >
> > def index(request):
> >     return HttpResponse("Hello, world. You're at the polls index.")
> > ```
>
> In other cases it is a global instance object you have to explicitly import
> and make use of, as in the case of `Flask` or `Bottle`:
>
> > ```python
> > from flask import request
> >
> > @app.route('/login', methods=['GET', 'POST'])
> > def login():
> >     if request.method == 'POST':
> >         do_the_login()
> >     else:
> >         show_the_login_form()
> > ```
>
> 2. Add a Response wrapper, which makes it easier to write correct responses.    As such, we don't have manually call `start_response` every time. Nor do
>    we remember that our return value is some kind of iterable.
>    Here is an example from `Flask`:
>
>    ```python
>    def index():
>       response = Response("Unicorns are OK")
>       response.headers['X-Parachutes'] = 'parachutes are cool'
>       response.set_cookie('username', 'the username')
>       return response
>    ```
>
> 3. Add some smart way of handling URL and request query parameters.
>    For example Django injects URL parameter to your application logic,
>    which allows you to make explicit use of them:
>
>    ```python
>    # in views.py
>    def detail(request, question_id):
>      return HttpResponse("You're looking at question %s." % question_id)
>
>    # in urls.py
>
>    from . import views
>
>    urlpatterns = [
>    # ex: /polls/
>    url(r'^$', views.index, name='index'),
>    # ex: /polls/5/
>    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
>    ...
>    ]
>    ```
>
> > Forms are processed and saved into a Dictionary like object,
> > [request.POST] and query data in saved into a [request.GET].
>
> 4. Add session and cookie management such that you manage some state.
>    Using cookies you can store information in the browser, for example
>    login cookie. And using sessions you can remember how the user
>    interacted with your website, for example you can remember the login date
>    and time.
> 5. Optionally, add HTML templating.
> 6. Optionally, add some persistency layer, e.g ORM or a NoSQL abstraction
>    layer.

Alas, we are not going to implement all those in just a couple of hours.
Instead, we are going to see how we can exploit Python's data model to build
convenient Python APIs for out Nano Python framework.
We start by implementing dictionary like session storage.

[request.get]: https://docs.djangoproject.com/en/1.11/ref/request-response/#django.http.HttpRequest.GET
[request.post]: https://docs.djangoproject.com/en/1.11/ref/request-response/#django.http.HttpRequest.POST
