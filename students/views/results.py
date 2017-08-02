# -*- coding: utf-8 -*-
from ..models import Exams, Result, Student, ResultsRegister

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def results_list(request):
    ''' Results list method '''

    # help variable:
    results_list = ResultsRegister.objects.all() # Results Register objects
    # Render Page:
    return render(request, 'students/results_list.html', {'results_list': results_list})

def results_register(request):
    ''' Results Register method '''
    # Help variable:
    exams_list = Exams.objects.all() # All Exams objects
    # FORM == POST:
    if request.method == 'POST':
        # Add button == PUSH:
        if request.POST.get('add_button') is not None:
            errors = {} # error collection
            # Exam Validation:
            exam = request.POST.get('exams_list')
            if not exam:
                errors['exams_list'] = u"Це поле є обов'язковим!"
            else:
                # Check if current Exam is registered :
                current_exam = ResultsRegister.objects.filter(exam=exam)
                if len(current_exam) > 0:
                    errors['exams_list'] = u"Цей іспить вже зареєстровано!"
                else:
                    exam = Exams.objects.get(id=exam)
            # Error == Fasle:
            if not errors:
                pass
                # add new Exam to Result Exam:
                result_register = ResultsRegister(exam=exam,view=True)
                result_register.save() # save in database
                # redirect to results list with success message:
                return HttpResponseRedirect(u"%s?status_message=Реєстрація Результату %s успішно завершено!" % (reverse('results_list'),result_register.exam))
            # Error == True:
            else:
                # Return Page with error and inpur data from user:
                return render(request, 'students/results_register.html',{'exams_list':exams_list,'errors':errors})
        # Cancel button == PUSH:
        elif request.POST.get('cancel_button') is not None:
            # Redirect to Results list page with cancel message:
            return HttpResponseRedirect(u'%s?status_message=Реєстрація Результату скасовано!' % reverse('results_list'))
    else:
        # Render Add Form Page:
        return render(request, 'students/results_register.html',{'exams_list':exams_list})

def result_list(request,eid):
    ''' Result method '''

    # help variables:
    students = Student.objects.all().order_by('last_name') # all Student objects sorted by Last Name
    eid = Exams.objects.get(id=eid) # Exams object with current id
    results = Result.objects.filter(exams_name=eid) # All Result objects for current Exams

    # Render Page:
    return render(request, 'students/result_list.html', {'students':students,'results':results,'eid':eid})

def result_view(request, eid, sid):
    ''' View Result method '''
    # help variables:
    eid = Exams.objects.get(id=eid) # Get current Exams
    sid = Student.objects.get(id=sid) # Get current Student
    # Check if Student have mark:
    try:
        # Student have mark == YES:
        result = Result.objects.get(exams_name=eid,student=sid) # return Result objects
    except Exception:
        # Student have mark == NO:
        result = 'Not Result' # return error as result

    # Render Page:
    return render(request, 'students/result_view.html',{'eid':eid,'sid':sid,'result':result})

def result_add(request,eid,sid):
    ''' Result to Results add '''
    # help variables:
    eid = Exams.objects.get(id=eid) # Get current Exams
    sid = Student.objects.get(id=sid) # Get current Student
    check = len(Result.objects.filter(exams_name=eid,student=sid)) # all Result with this student and exam name

    # Result already exist == False:
    if check == 0:
        # FORM == POST:
        if request.method == 'POST':
            # Add Button == PUSH:
            if request.POST.get('add_button') is not None:
                data = {} # data collection
                errors = {} # error colelction

                # add not validation data:
                data = {'exams_name':eid,'student':sid}

                # Mark validation:
                mark = request.POST.get('mark')
                if not mark:
                    errors['mark'] = u"Виберыіть оцінку, будь-ласка."
                else:
                    if int(mark) <= 0:
                        errors['mark'] = u"Мінімальна оцінка може бути 1"
                    elif int(mark) >= 41:
                        errors['mark'] = u"Максимальна оцінка може бути 40"
                    else:
                        data['mark'] = mark

                # Error == False:
                if not errors:
                    # create new Result object:
                    new_result = Result(**data)
                    # save this object in database:
                    new_result.save()
                    # redirect to result list with success message:
                    return HttpResponseRedirect(u"%s?status_message=Оцінку %s для студенту %s додано!" % (reverse('result_list', kwargs={'eid':eid.id}), new_result.mark, new_result.student))
                # Error == True:
                else:
                    # render Form with error and input from user:
                    return render(request,'students/result_add.html', {'eid':eid, 'sid':sid,'errors':errors})
            # Cancel Button == PUSH:
            elif request.POST.get('cancel_button') is not None:
                # redirect to result list page with cancel message:
                return HttpResponseRedirect(u"%s?status_message=Додавання оцінки скасовано! " % reverse('result_list', kwargs={'eid':eid.id}))
        else:
            # Render Page:
            return render(request,'students/result_add.html', {'eid':eid, 'sid':sid})
    # Result already exist == True:
    else:
        # redirect to result list page with error message:
        return HttpResponseRedirect(u"%s?status_message=Оцінка для студунта %s вже існує" % (reverse('result_list', kwargs={'eid':eid.id}), sid))
