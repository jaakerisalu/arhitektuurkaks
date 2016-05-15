import json

from django.core.urlresolvers import reverse_lazy
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponseNotFound, JsonResponse, HttpResponseServerError
from django.template import TemplateDoesNotExist, Engine, Context, loader
from django.utils.translation import gettext as _
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import ListView, DetailView, UpdateView

from arhitektuurkaks.helpers import fake_log
from arhitektuurkaks.models import Tvseries


def sentry_id_from_request(request):
    if getattr(request, 'sentry', None) is not None:
        return request.sentry.get('id', None)

    return None


def page_not_found(request, template_name='404.html'):
    context = {
        'request_path': request.path,
        'error': {
            'title': _('Page not found'),
            'message': _("We tried but couldn't find this page, sorry."),
        },
    }

    try:
        template = loader.get_template(template_name)
        body = template.render(context, request)
        content_type = None

    except TemplateDoesNotExist:
        template = Engine().from_string(
            '<h1>Not Found</h1>'
            '<p>The requested URL {{ request_path }} was not found on this server.</p>')
        body = template.render(Context(context))
        content_type = 'text/html'

    return HttpResponseNotFound(body, content_type=content_type)


@requires_csrf_token
def server_error(request, template_name='500.html'):
    if request.is_ajax() or request.META.get('HTTP_ACCEPT', 'text/plain') == 'application/json':
        return JsonResponse({
            'sentry': sentry_id_from_request(request),
            'error': {
                'title': _('Something went wrong'),
            }
        }, status=500)

    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return HttpResponseServerError('<h1>Server Error (500)</h1>', content_type='text/html')

    return HttpResponseServerError(template.render({
        'sentry': sentry_id_from_request(request),
        'error': {
            'title': _('Something went wrong'),
            'message': ('%s' % _('Something went wrong on our side... \n Please hold on while we fix it.')).replace('\n', '<br>'),
            'sentry': _('Fault code: #'),
        }
    }))


class TvSeriesView(ListView):
    template_name = 'series.html'
    model = Tvseries

    def get(self, request, *args, **kwargs):
        fake_log("Getting a list of all TV Series")
        return super().get(request, *args, **kwargs)


class TvSeriesDetailView(DetailView):
    template_name = 'series-detail.html'
    model = Tvseries

    def get_object(self, queryset=None):
        obj = Tvseries.objects.get(id=self.kwargs['series_id'])
        return obj

    def get(self, request, *args, **kwargs):
        fake_log("Getting Detail view of series: {}".format(self.get_object().name))
        return super().get(request, *args, **kwargs)


class TvSeriesEditView(UpdateView):
    template_name = 'series-edit.html'
    model = Tvseries
    success_url = reverse_lazy('series')
    fields = ["name", "season", "description"]

    def get_object(self, queryset=None):
        obj = Tvseries.objects.get(id=self.kwargs['series_id'])
        return obj

    def get(self, request, *args, **kwargs):
        fake_log("Editing of series: {}".format(self.get_object().name))
        return super().get(request, *args, **kwargs)


def get_object(request):
    try:
        obj_id = request.GET.get('id', None)
        if id:
            obj = Tvseries.objects.get(id=obj_id)
            fake_log("API access of series: {}".format(obj.name))
        else:
            fake_log("API error: no 'id' parameter")
            return JsonResponse({'error': "Please add a query (api/?id=xxx)"})
    except Tvseries.DoesNotExist:
        fake_log("API error: Object not found")
        return JsonResponse({'error': "Object does not exist"})

    return JsonResponse(model_to_dict(obj))
