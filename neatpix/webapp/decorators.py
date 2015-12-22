from functools import wraps
from django.http import JsonResponse


def json_response(func):
    """
    View decorator function that converts the dictionary response
    returned by a view function to django JsonResponse.
    """
    @wraps(func)
    def func_wrapper(request, *args, **kwargs):
        return JsonResponse(func(request, *args, **kwargs))

    return func_wrapper
