from django.shortcuts import render
from django.views.generic import ListView, FormView, CreateView, TemplateView, DeleteView
from django.views import View
from .models import Conteudo, Manga, Arquivos, Capitulos
from .forms import FormularioManga
from django.shortcuts import redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from rest_framework import generics
from .serialize import mangaSerializer, mangaDetalhes, capituloDetalhes, pgDetalhes, totalSere
from rest_framework.views import APIView
from rest_framework.response import Response


class listarAPI(generics.ListCreateAPIView):
    queryset = Manga.objects.all()
    serializer_class = mangaSerializer

class mangaInfoAPI(APIView):

    def get_object(self, pk):
        try:
            mg = Manga.objects.get(pk=pk)
            cp = Capitulos.objects.filter(manga=pk)
            obj = {'manga': mg, 'cap': cp}
            return obj
        except Manga.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        snippet = self.get_object(pk)
        serializer = mangaDetalhes(snippet)
        return Response(serializer.data)


class mangaDelete(DeleteView):
    model = Manga
    template_name = 'addConteudo/deletarMG.html'

    def get_success_url(self, **kwargs):
        if kwargs != None:
            return reverse_lazy('usuario:perfil', kwargs={'pk': self.object.autor.id})
        else:
            return reverse_lazy('usuario:perfil', args=(self.object.autor.id,))


class capDelete(TemplateView):
    model = Capitulos
    template_name = 'addConteudo/deletarCP.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manga = Manga.objects.get(pk=kwargs['pk'])
        cap = Capitulos.objects.get(manga=manga, cpN=kwargs['cp'])
        context['manga'] = manga
        context['cap'] = cap

        return context

    def post(self, request, pk, cp):
        aux = Capitulos.objects.get(manga=pk, cpN=cp)
        aux.delete()
        return(redirect('/add/manga/{0}/'.format(pk)))

class CapituloInfoAPI(APIView):

    def get_object(self, pk, cp):
        try:
            cap = Capitulos.objects.get(manga=pk, cpN=cp)
            arq = Arquivos.objects.filter(capitulo=cap.id)
            obj = {'cap': cap, 'arq': arq}
            return obj
        except Capitulos.DoesNotExist:
            raise Http404
    def get(self, request, pk, cp):
        snippet = self.get_object(pk, cp)
        serializer = capituloDetalhes(snippet)
        return Response(serializer.data)


    
# Create your views here.
class postList(ListView):
    model = Conteudo
    paginate_by = 100
    template_name = 'addConteudo/inicio.html'



class postManga(CreateView):  

    model = Manga
    form_class = FormularioManga
    template_name = 'addConteudo/manga.html'

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

    def get_success_url(self, **kwargs):
        print(self.object.id)
        if kwargs != None:
            return reverse_lazy('add:addCap', kwargs={'pk': self.object.id})
        else:
            return reverse_lazy('add:addCap', args=(self.object.id,))



class lista(TemplateView):

    model = Manga
    template_name = 'addConteudo/lista.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['manga'] = Manga.objects.order_by('dtp')

        return context


class mangaInfo(TemplateView):

    model = Manga
    template_name = 'addConteudo/mangaInfo.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['manga'] = Manga.objects.get(pk=kwargs['pk'])
        context['cap'] = Capitulos.objects.filter(manga=kwargs['pk'])

        return context

class verCap(TemplateView):

    model = Arquivos
    template_name = 'addConteudo/verCap.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manga = Manga.objects.get(pk=kwargs['pk'])
        cap = Capitulos.objects.get(manga=manga, cpN=kwargs['cp'])
        arq = Arquivos.objects.filter(capitulo=cap)
        capa = Arquivos.objects.get(capitulo=cap, ordem=0)
        context['cap3'] = Capitulos.objects.filter(manga=kwargs['pk'])
        context['manga'] = manga
        context['cap'] = cap
        context['cap2'] = arq
        context['total'] = len(arq)
        context['capa'] = capa

        return context


class verPg(TemplateView):

    model = Arquivos
    template_name = 'addConteudo/verPg.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manga = Manga.objects.get(pk=kwargs['pk'])
        cap = Capitulos.objects.get(manga=manga, cpN=kwargs['cp'])
        arq = Arquivos.objects.filter(capitulo=cap)
        pg = Arquivos.objects.get(capitulo=cap, ordem=kwargs['pg'])
        context['manga'] = manga
        context['cap'] = cap
        context['cap2'] = arq
        context['pg'] = pg
        context['anterior'] = kwargs['pg'] - 1
        context['proximo'] = kwargs['pg'] + 1
        context['total'] = len(arq)
        return context

class pgAPI(APIView):

    def get_object(self, pk, cp, pg):
        try:
            cap = Capitulos.objects.get(manga=pk, cpN=cp)
            total = Arquivos.objects.filter(capitulo=cp)
            arq = Arquivos.objects.get(capitulo=cp, ordem=pg)
            obj = {'cap': cap, 'arq': arq}
            return obj
        except Capitulos.DoesNotExist:
            raise Http404
    def get(self, request, pk, cp, pg):
        snippet = self.get_object(pk, cp, pg)
        serializer = pgDetalhes(snippet)
        return Response(serializer.data)

class addCap(TemplateView):
    
    template_name = 'addConteudo/addCap.html'
    model = Capitulos
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(len(Capitulos.objects.filter(manga=kwargs['pk'])))
        context['cap'] = Capitulos.objects.filter(manga=kwargs['pk'])
        return context

    def post(self, request, pk):
        fs = FileSystemStorage()
        i = 0
        cp = Capitulos()
        cp.manga = Manga.objects.get(pk=pk)
        cp.cpN = self.request.POST.get('capitulo')
        cp.titulo = self.request.POST.get('titulo')
        cp.resumo = self.request.POST.get('resumo')
        cp.save()
        arq = request.FILES.getlist('pro-image')
        for aux in arq:
            aux1 = fs.save('mangas/manga_{0}/capitulo_{1}/{2}'.format(pk, cp.cpN, aux.name), aux)
            caminho = fs.url('../'+aux1)
            if i == 0:
                cp2 = Capitulos.objects.get(pk=cp.id)
                cp2.capa = caminho+''
                cp2.save()
            aq = Arquivos(capitulo = cp)
            aq.aquivos = caminho
            aq.ordem = i
            aq.save()
            i+=1
        return(redirect('/add/manga/{0}/'.format(pk)))

class edtCap(TemplateView):

    model = Arquivos
    template_name = 'addConteudo/edtCap.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manga = Manga.objects.get(pk=kwargs['pk'])
        cap = Capitulos.objects.get(manga=manga, cpN=kwargs['cp'])
        arq = Arquivos.objects.filter(capitulo=cap)
        capa = Arquivos.objects.get(capitulo=cap, ordem=0)
        context['cap3'] = Capitulos.objects.filter(manga=kwargs['pk'])
        context['manga'] = manga
        context['cap'] = cap
        context['cap2'] = arq
        context['total'] = len(arq)
        context['capa'] = capa

        return context
