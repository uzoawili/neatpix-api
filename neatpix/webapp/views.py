from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View


class LoginRequiredMixin(object):
    """
    View mixin which requires that the user is authenticated.
    """
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class IndexView(View):
    """
    Represents the index/authentication view.
    """

    def get(self, request, *args, **kwargs):
        """
        Renders the index/home view
        """
        # redirect to dashboard if user is already signed in:
        if request.user.is_authenticated():
            return redirect(reverse('webapp:dashboard'))
        # show index view:
        context = {}
        context.update(csrf(self.request))
        return render(self.request, 'webapp/index.html', context)


class LogoutView(LoginRequiredMixin, View):
    """
    Logs the user out.
    """

    def get(self, request, *args, **kwargs):
        """
        Logs a user out and redirects to the index view.
        """
        logout(request)
        return redirect(reverse('webapp:index'))


class DashboardView(LoginRequiredMixin, View):
    """
    Represents the signed in users' dashboard/workspace view.
    """

    def get(self, request, *args, **kwargs):
        """
        Renders the dashboard view.
        """
        # show index view:
        context = {}
        context.update(csrf(self.request))
        return render(self.request, 'webapp/dashboard.html', context)
