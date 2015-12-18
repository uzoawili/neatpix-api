from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.views.generic import View


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


class DashboardView(View):
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
        return render(self.request, 'webapp/index.html', context)
