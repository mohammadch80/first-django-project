from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from .models import Students, Group
from django.db.models import F
from django.views import generic


def index(request):
    groups = Group.objects.all().values()
    template = loader.get_template('index.html')
    context = {
        'groups': groups,
    }
    return HttpResponse(template.render(context, request))


def add(request):
    template = loader.get_template('add.html')
    return HttpResponse(template.render({}, request))


def add_student(request):
    name = request.POST['name']
    age = request.POST['age']
    try:
        group = Group.objects.get(name=request.POST['group'])
    except Group.DoesNotExist:
        return HttpResponse('The group with this name does not exist.')
    member = Students(name=name, age=age, group=group)
    member.save()
    return HttpResponseRedirect(reverse('students:index'))


def add_group(request):
    name = request.POST['name']
    birth = request.POST['birth']
    if Group.objects.filter(name=name):
        return HttpResponse('There is another group with this name.')
    member = Group(name=name, birth_year=birth)
    member.save()
    return HttpResponseRedirect(reverse('students:index'))


def delete_student(request, id):
    try:
        member = Students.objects.get(id=id)
    except Students.DoesNotExist:
        raise Http404("Student does not exist")
    group_id = member.group.id
    member.delete()
    return HttpResponseRedirect(reverse('students:group_detail', args=(group_id,)))


def update_student(request, group_id, id):
    stu = get_object_or_404(Students, pk=id)
    return render(request, "update.html", {"my_student": stu})


def update_record(request, group_id, id):
    name = request.POST['name']
    age = request.POST['age']
    score = request.POST['score']
    member = get_object_or_404(Students, id=id)
    member.name = name
    member.age = age
    member.score = score
    member.save()
    return HttpResponseRedirect(reverse('students:group_detail', args=(group_id,)))


def group_detail(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    ordered_students = group.students_set.order_by("-score")
    return render(request, "group_detail.html", {"group": group, 'ordered_students': ordered_students})


def vote_list(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    return render(request, "vote.html", {"group": group},)


def vote(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    check_list = request.POST.getlist("students")
    selected_students = [group.students_set.get(pk=id) for id in check_list]
    if not selected_students:
        return render(
            request,
            "vote.html",
            {
                "group": group,
                "error_message": "No one is selected.",
            },
        )
    else:
        for stu in selected_students:
            stu.score = F('score') + 1
            stu.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("students:group_detail", args=(group_id,)))