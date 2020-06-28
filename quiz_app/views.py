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
        time = request.GET.get('time')
        ques = Questions.object.all()
        if start and candidate:
            contestant_id = User.objects.get(username=candidate).id
            a = UserAnswerDetails.object.filter(contestant_id=contestant_id)
            sum_of_score = a.aggregate(score=Sum('score'))
            if sum_of_score['score'] and sum_of_score['score'] > 7:
                result = 'Pass'
            else:
                result = 'Fail'
            try:
                if a.get(end_quiz=True):
                    return render(request, 'quiz_details.html', {'end_quiz': 'end_quiz', 'sum_of_score': sum_of_score['score'],
                                                         'result': result})
            except ObjectDoesNotExist:
                return render(request, 'quiz_details.html', {'start': 'start'})
        elif (q_id != '' or q_id is not None) and not end and not option:
            ques = ques.get(id=int(q_id))
            t = [00,00]
            if time:
                t = list(map(int, time.split(':')))
            else:
                t = [60, 10]
            return JsonResponse({'id': ques.id, 'question': ques.question, 'options': [ques.A, ques.B,
                                                      ques.C, ques.D], 'minutes': t[0], 'seconds': t[1]}, status=200)
        elif (q_id != '' or q_id is not None) and option is not None and candidate:
            ans = ques.get(id=int(q_id))
            right_ans = ans.answer
            explanation = ans.explanation
            contestant_id = User.objects.get(username=candidate).id
            a = UserAnswerDetails.object.filter(contestant_id=contestant_id)
            if ans.question:
                try:
                    if ans.question == a.get(question=ans.question).question:
                        return JsonResponse({'msg': 'You have already submitted your answer', 'ans': a.get(question=ans.question).answer}, status=200)
                except ObjectDoesNotExist:
                    pass
            if right_ans == option:
                save_ans = a.create(question=ans.question, answer=option, score=1, time=time, contestant_id=contestant_id)
                save_ans.save()
                b = UserAnswerDetails.object.filter(contestant_id=contestant_id).get(answer=ans.answer)
                return JsonResponse({'msg': 'Your answer is right', 'ans': b.answer}, status=200)
            elif right_ans != option:
                a = a.create(question=ans.question, answer=option, score=0, time=time, contestant_id=contestant_id)
                a.save()
                return JsonResponse({'answer': right_ans, 'explanation': explanation}, status=200)

        if end:
            contestant_id = User.objects.get(username=candidate).id
            last_data = UserAnswerDetails.object.filter(contestant_id=contestant_id)
            last_data.create(contestant_id=contestant_id, end_quiz=True).save()
            sum_of_score = last_data.aggregate(score=Sum('score'))
            if sum_of_score['score'] and sum_of_score['score'] > 7:
                result = 'Pass'
            else:
                result = 'Fail'
            time = list(map(int, time.split(':')))
            time = str(9 - time[0]) + ':' + str(60 - time[1])
            return render(request, 'quiz_details.html', {'end_quiz': 'end_quiz', 'sum_of_score': sum_of_score['score'],
                                                         'time': time, 'result': result})
    return render(request, 'quiz_details.html')


