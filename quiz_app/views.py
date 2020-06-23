import json
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET
from .forms import RegisterForm, SignIn
from .models import Questions, UserAnswerDetails
from django.db.models import Avg, Count, Min, Sum
from django.core.exceptions import ObjectDoesNotExist



@csrf_exempt
def signup(request):
    err = ''
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.data['psw'] == form.data['psw_repeat']:
            if form.is_valid():
                user = User.objects.create_user(first_name=form.data['first_name'], last_name=form.data['last_name'],
                                                username=form.data['username'], email=form.data['email'],
                                                password=form.data['psw_repeat'])
                user.save()
                return HttpResponseRedirect('/signin')
            else:
                err = 'Invalid login please try again'
        else:
            err = 'Password does not match please try again'
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form, 'err': err})


@csrf_exempt
def signin(request):
    err = ''
    if request.method == 'POST':
        form = SignIn(request.POST)
        if authenticate(username=form.data['username'], password=form.data['psw']):
            user = User.objects.get(username=form.data['username'])
            # return HttpResponseRedirect('/quiz_details')
            return quiz_details(request, user.first_name)
        else:
            err = 'Invalid username or password'
    else:
        form = SignIn()
    return render(request, 'signin.html', {'form': form, 'err': err})


@require_http_methods(["GET", "POST"])
def quiz_details(request, user):
    return render(request, 'quiz_details.html', {'user': user})


@require_http_methods(["GET", "POST"])
def start_quiz(request):
    if request.method == 'GET':
        start = request.GET.get('s_quiz')
        q_id = request.GET.get('q_id')
        end = request.GET.get('end_quiz')
        option = request.GET.get('option')
        candidate = request.GET.get('candidate')
        ques = Questions.object.all()
        if start:
            return render(request, 'quiz_details.html', {'start': 'start'})
        elif (q_id != '' or q_id is not None) and not end and not option:
            ques = ques.get(id=int(q_id))
            return JsonResponse({'id': ques.id, 'question': ques.question, 'options': [ques.A, ques.B,
                                                      ques.C, ques.D]}, status=200)
        elif (q_id != '' or q_id is not None) and option is not None and candidate:
            ans = ques.get(id=int(q_id))
            right_ans = ans.answer
            explanation = ans.explanation
            contestant_id = User.objects.get(username=candidate).id
            a = UserAnswerDetails.object.filter(contestant_id=contestant_id)
            if ans.question:
                try:
                    if ans.question == a.get(question=ans.question).question:
                        return JsonResponse({'msg': 'You have already submitted your answer'}, status=200)
                except ObjectDoesNotExist:
                    pass
            if right_ans == option:
                a = a.create(question=ans.question, answer=option, score=1, contestant_id=contestant_id)
                a.save()
                return JsonResponse({'msg': 'Your answer is right'}, status=200)
            elif right_ans != option:
                a = a.create(question=ans.question, answer=option, score=0, contestant_id=contestant_id)
                a.save()
                return JsonResponse({'answer': right_ans, 'explanation': explanation}, status=200)
        else:
            contestant_id = User.objects.get(username=candidate).id
            sum_of_score = UserAnswerDetails.object.filter(contestant_id=contestant_id).aggregate(score=Sum('score'))
            print(sum_of_score)
            return render(request, 'quiz_details.html', {'end_quiz': 'end_quiz', 'sum_of_score': sum_of_score['score']})

    return render(request, 'quiz_details.html', {'id': ques.id, 'question': str(ques.id) +'. '+ ques.question, 'options': [ques.A, ques.B,
                                                      ques.C, ques.D], 'time': '10:00'})


