from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.detail import DetailView
from .models import Documentary, Site, Report

class DocumentaryDetailView(DetailView):
    model = Documentary

    def get_template_names(self):
        return 'documentaries/detail.html'

class ToSiteRedirectView(RedirectView):
    def get_redirect_url(self, **kwargs):
        url = get_object_or_404(Site, id=kwargs.get('id'))
        url.add_visitor()
        return url.url

class AboutView(TemplateView):
    def get_template_names(self):
        return "documentaries/about.html"

class ReportDocumentaryView(View):
    def post(self, request):
        print(request.POST.get('site'))
        site = get_object_or_404(Site, id=request.POST.get('site'))
        data = {
            "site": site,
            "comment": request.POST.get('comment')
        }
        Report.objects.create(**data)
        return redirect(request.META.get('HTTP_REFERER'))

class SearchDocumentaryView(View):
    def get(self, request):
        # Obtener palabras por buscar.
        words = request.GET.get('query')
        documentaries = []
        if words:
            documentaries = self.__get_documentaries_in_search(words)
        else:
            # Retornar todos los documentales.
            documentaries = Documentary.objects.all()
        # Paginar el restultado.
        elements = self.__get_documentaries_per_page(request, documentaries)
        # Retornar documentales y palabras por buscar.
        context = {
            "documentaries": elements,
            "words": words if words else ''
        }
        return render(request, 'documentaries/search.html', context)

    @classmethod
    def __get_documentaries_per_page(cls, request, documentaries):
        paginator = Paginator(documentaries, 24)
        page = request.GET.get('page')
        return paginator.get_page(page)

    @classmethod
    def __get_documentaries_in_search(cls, words):
        # Crear vector con palabras para buscar.
        query_words = [word.strip() for word in words.split(' ') if word]
        # Retornar documentaries.
        documentaries = Documentary.objects.search(query_words)
        # Guardar resultados.
        # search.documentaries.set(documentaries)
        return documentaries