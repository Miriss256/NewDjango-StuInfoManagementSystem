import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from manager.views import StudentAddForm
from manager import models as manager_models

logger = logging.getLogger(__name__)


def teacher_index(request):
    """学生列表"""
    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict["studentid__contains"] = search_data

    obj_list = manager_models.student.objects.filter(**data_dict).order_by("-grade")  # 返回数据库信息
    return render(request, "teacher/teacher_index.html", {"obj_list": obj_list})

def student_info(request, uid):
    """学生详情"""
    obj = manager_models.student.objects.get(studentid=uid)  # 返回查询信息
    return render(request, "teacher/teacher_student_info.html", {"obj": obj})


def student_add(request):
    """学生添加"""
    if request.method == "GET":  # 设置默认响应页面
        form = StudentAddForm()
        return render(request, "teacher/teacher_student_add.html", {"form": form})

    form = StudentAddForm(data=request.POST, files=request.FILES)  # 获取web端提交的数据
    if form.is_valid():  # 如果数据合法就保存
        form.save()
        return redirect("/teacher/index/")

    return render(
        request, "teacher/teacher_student_add.html", {"form": form}
    )  # 提交数据不合法返回默认页面


def student_edit(request, uid):
    """学生信息修改"""
    row_object = manager_models.student.objects.filter(
        studentid=uid
    ).first()  # 获取请求的数据的值
    if request.method == "GET":  # 默认响应页面
        form = StudentAddForm(instance=row_object)
        return render(request, "teacher/teacher_student_edit.html", {"form": form})
    form = StudentAddForm(data=request.POST, files=request.FILES, instance=row_object)
    if form.is_valid():  # 如果数据合法就保存
        form.save()  # 更新数据
        return redirect("/teacher/index/")  # 返回列表页面
    return render(
        request, "teacher/teacher_student_edit.html", {"form": form}
    )  # 提交数据不合法返回默认页面


def student_delete(request):
    """删除学生"""
    uid = request.GET.get("uid")
    logger.debug("teacher delete uid=%s", uid)
    if not manager_models.student.objects.filter(studentid=uid).exists():
        return JsonResponse({"status": False, "error": "删除失败，数据不存在"})

    manager_models.student.objects.filter(studentid=uid).delete()
    return JsonResponse({"status": True})

def teacher_info(request):
    """教师详情"""
    id = request.session["info"]["id"]
    obj = manager_models.teacher.objects.get(id=id)  # 返回查询信息
    return render(request, "teacher/teacher_info.html", {"obj": obj})