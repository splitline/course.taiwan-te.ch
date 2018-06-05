from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render_to_response

from parser.models import Courses
from userData.models import SelectedCourse

def timetable(request):
    DAYS = {
        "M": 1,
        "T": 2, 
        "W": 3, 
        "R": 4,
        "F": 5, 
        "S": 6, 
        "U": 7, 
    }
    TIMES = {
        '0':  '07:10-08:00',
        '1':  '08:10-09:00',
        '2':  '09:10-10:00',
        '3':  '10:20-11:10',
        '4':  '11:20-12:10',
        '5':  '12:20-13:10',
        '6':  '13:20-14:10',
        '7':  '14:20-15:10',
        '8':  '15:30-16:20',
        '9':  '16:30-17:20',
        '10': '17:30-18:20',
        'A':  '18:25-19:15',
        'B':  '19:20-20:10',
        'C':  '20:10-21:05',
        'D':  '21:10-22:00'
    }
    if request.user.is_authenticated:
        selectedCourses = SelectedCourse.objects.filter(user=request.user, type=1)
    return render_to_response("index.html", locals())

def search_api(request):
    result = {}
    if 'keyword' in request.GET and 'semester' in request.GET:
        keyword = request.GET['keyword']
        result = Courses.objects.filter(
            (Q(name__contains = keyword) |
            Q(lecturer__contains=keyword) |
            Q(course_id__contains = keyword)) &
            Q(semester = request.GET['semester'])
        )
    return HttpResponse(serializers.serialize('json', result), content_type='application/json')

def get_course_api(request):
    result = {}
    if 'courseno' in request.GET and 'semester' in request.GET:
        courseno = request.GET['courseno']
        semester = request.GET['semester']
        result = Courses.objects.get(id = semester + courseno)
    return HttpResponse(serializers.serialize('json', result), content_type='application/json')


def add_api(request):
    if request.user.is_authenticated and 'courseno' in request.GET:
        courseno = request.GET['courseno']
        # profile = UserProfile.objects.get(user = request.user)
        course = Courses.objects.get(id = courseno)
        print(course)
        sc = SelectedCourse(
            user = request.user,
            course = course,
            type = ('favorite' in request.GET) + 1 # 1:SELECT / 2:FAVORITE
        )
        sc.save()
        return HttpResponse(serializers.serialize('json', [course]), content_type='application/json')
    print(request.user, request.user.is_authenticated , 'courseno' in request.GET)
    return JsonResponse({"Result":"Error"})

def del_api(request):
    if request.user.is_authenticated and 'courseno' in request.GET:
        courseno = request.GET['courseno']
        # profile = UserProfile.objects.get(user = request.user)
        course = Courses.objects.get(id = courseno)
        sc = SelectedCourse.objects.filter(user = request.user, course=course, type = ('favorite' in request.GET) + 1)
        sc.delete()
        return JsonResponse({"Result":"Success"})
    print(request.user, request.user.is_authenticated , 'courseno' in request.GET)
    return JsonResponse({"Result":"Error"})