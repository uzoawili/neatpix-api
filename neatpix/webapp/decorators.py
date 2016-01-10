from functools import wraps
from django.http import JsonResponse


def json_response(func):
    """
    View decorator function that converts the dictionary response
    returned by a view function to django JsonResponse.
    """
    @wraps(func)
    def func_wrapper(request, *args, **kwargs):
        func_response = func(request, *args, **kwargs)
        status_code = func_response.get('status_code', 200)
        return JsonResponse(func_response, status=status_code)

    return func_wrapper
