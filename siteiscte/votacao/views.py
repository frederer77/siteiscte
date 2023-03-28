from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView
from .models import Questao, Opcao, Aluno


@login_required(login_url='votacao/login')
def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'votacao/index.html', context)


@login_required(login_url='votacao/login')
def criarquestao(request):
    if request.method == 'POST':
        try:
            questao_texto = request.POST.get("texto")
        except KeyError:
            return render(request, 'votacao/criarquestao.html')
        if questao_texto:
            questao = Questao(questao_texto=questao_texto,
                              pub_data=timezone.now())
            questao.save()
            return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))
        else:
            return HttpResponseRedirect(reverse('votacao:criarquestao'))
    else:
        return render(request, 'votacao/criarquestao.html')


@login_required(login_url='votacao/login')
def eliminarQuestao(request):
    questoes = Questao.objects.all()
    print(questoes)
    return render(request, 'votacao/eliminarQuestao.html', {'questoes': questoes})


@login_required(login_url='votacao/login')
def eliminar(request):
    try:
        questao_seleccionada = Questao.objects.get(pk=request.POST['questao'])
    except (KeyError, Questao.DoesNotExist):
        # Apresenta de novo o form para votar
        questoes = Questao.objects.all()
        return render(request, 'votacao/eliminarQuestao.html',
                      {'questoes': questoes, 'error_message': "Não escolheu uma opção", })
    else:
        questao_seleccionada.delete()
    return HttpResponseRedirect(reverse('votacao:index'))


@login_required(login_url='votacao/login')
def detalhe(request, questao_id):
    questao = Questao.objects.get(pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})


@login_required(login_url='votacao/login')
def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})


@login_required(login_url='votacao/login')
def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html', {
            'questao': questao,
            'error_message': "Não escolheu uma opção",
        })
    else:
        if 'eliminarOpcao' in request.POST:
            opcao_seleccionada.delete()
            return render(request, 'votacao/detalhe.html', {'questao': questao, })
        if not request.user.is_superuser:
            try:
                if 26 > request.user.aluno.votos:
                    request.user.aluno.adicionar_voto()
                    opcao_seleccionada.votos += 1
                    opcao_seleccionada.save()
            except ValueError:
                return render(request, 'votacao/detalhe.html', {'questao': questao, 'error_message': "Num de grupo invalido", })
        else:
            opcao_seleccionada.votos += 1
            opcao_seleccionada.save()
        return HttpResponseRedirect(
            reverse('votacao:resultados', args=(questao.id,))
        )


@login_required(login_url='votacao/login')
def criaropcao(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/criaropcao.html', {'questao': questao})


@login_required(login_url='votacao/login')
def eliminarOpcao(request, opcao_id):
    opcao = get_object_or_404(Opcao, pk=opcao_id)
    opcao.delete()
    return HttpResponseRedirect(reverse('votacao:index'))


@login_required(login_url='votacao/login')
def save_option(request, questao_id):
    if request.method == 'POST':
        q = Questao.objects.get(pk=questao_id)
        q.opcao_set.create(opcao_texto=request.POST['texto'], votos=0)
        return HttpResponseRedirect(reverse('votacao:index'))


def criarAluno(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            curso = request.POST.get('curso')
            password = request.POST.get('password')
        except KeyError:
            return render(request, 'votacao/criarAluno.html')

        if nome and email and curso and password:
            user = User.objects.create_user(nome, email, password)
            user.save()
            aluno = Aluno.objects.create(user=user, curso=curso)
            aluno.save()
            return HttpResponseRedirect(reverse('votacao:login'))
        else:
            return HttpResponseRedirect(reverse('votacao:criarAluno'))
    else:
        return render(request, 'votacao/criarAluno.html')


def loginview(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            password = request.POST.get('password')
        except KeyError:
            return render(request, 'votacao/login.html')

        if nome and password:
            user = authenticate(username=nome, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('votacao:index'))
            else:
                return HttpResponseRedirect(reverse('votacao:criarAluno'))
    else:
        return render(request, 'votacao/login.html')


@login_required(login_url='votacao/login')
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:login'))


@login_required(login_url='votacao/login')
def detalheAluno(request):
    return render(request, 'votacao/detalheAluno.html')