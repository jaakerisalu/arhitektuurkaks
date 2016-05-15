# README for Arhitektuuri Labor 

## Doing the minimum possible

I tried to use Django (besides logging) to the fullest on this one

### The logging

I went for the easy way out: A log file in a publicly accessible directory (static) and adding entries manually

```
    def fake_log(string):
        with open("**FILE LOCATION**", "a") as text_file:
            print("[{}]: {}".format(datetime.datetime.now().strftime("%H:%M @ %d/%m/%y"), string), file=text_file)
        text_file.close()
```

This provides me with a nice log

```
    [17:04 @ 15/05/16]: Editing of series: Vikings
    [17:04 @ 15/05/16]: Getting a list of all TV Series
    [17:22 @ 15/05/16]: API access of series: House of Cardzo
    [17:23 @ 15/05/16]: API access of series: House of Cardzo
    [17:23 @ 15/05/16]: API error: Object not found
    [17:25 @ 15/05/16]: API error: no 'id' parameter
```

### The URLS

All functionality, List view, Detail view, and Edit view can be mapped to the same user-friendly tree:

```python
    urlpatterns = [
        url(r'', include('accounts.urls')),
        url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
        url(r'^s/$', TvSeriesView.as_view(), name='series'),
        url(r'^s/(?P<series_id>\d+)/$', TvSeriesDetailView.as_view(), name='series-detail'),
        url(r'^s/(?P<series_id>\d+)/edit/$', TvSeriesEditView.as_view(), name='series-edit'),
    
        url(r'^tagauks/', include(admin.site.urls)),
    ]
```
  
### The Views

Django has built-in basic class based views for all 3 functionalities:

```python
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
```

### The Templates

Finally, the templates get access to special context automatically provided by the views:

- The List view template gets {{ object_list }}

- The Detail view template gets {{ object }}

- The Edit view template gets {{ form }}

### The API

For the API I just went with a simple function that returns a serialized object with some error handling

**urls.py**

```python
    url(r'^api/', views.get_object, name='series-api')
```

**views.py**

```python
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
```




