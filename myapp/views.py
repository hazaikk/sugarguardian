import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from myapp.models import Prediction, Body


# Create your views here.
class PredictionCreate(LoginRequiredMixin, CreateView):
    template_name = 'myapp/prediction.html'
    success_url = 'result'
    model = Prediction
    fields = ['gender', 'year', 'tall', 'weight', 'family', 'press', 'test', 'release', 'thick']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.applicant = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class DataCreate(LoginRequiredMixin, CreateView):
    template_name = 'myapp/data.html'
    success_url = 'body/1'
    model = Body
    fields = ['bmi', 'heart', 'ssy', 'szy', 'bl', 'bg', 'bone', 'muscle', 'diary']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@login_required  # 限制只有登录了才能访问
def build(request):
    return render(request, 'myapp/pages/404.html')


def login(request):
    return redirect('accounts/login')


@login_required  # 限制只有登录了才能访问
def profile(request):
    return render(request, 'account/profile.html')


@login_required  # 限制只有登录了才能访问
def doctor(request):
    return render(request, 'myapp/doctor.html')


@login_required  # 限制只有登录了才能访问
def visual(request):
    # 查询产品数据
    datas = Body.objects.filter(user=request.user)
    # 构建饼图数据
    bmi, heart, ssy, szy, bl, bg, bone, muscle, date= [],[],[],[],[],[],[],[], []
    for d in datas:
        date.append(d.created_date.strftime('%Y-%m-%d'))
        bmi.append(d.bmi)
        heart.append(d.heart)
        ssy.append(d.ssy)
        szy.append(d.szy)
        bl.append(d.bl)
        bg.append(d.bg)
        bone.append(d.bone)
        muscle.append(d.muscle)
    # 'bmi', 'heart', 'ssy', 'szy', 'bl', 'bg', 'bone', 'muscle', 'diary'
    # 将数据转换为JavaScript代码块期望的格式
    context = {
        'date':date,
        'bmi':bmi,
        'heart':heart,
        'ssy':ssy,
        'szy':szy,
        'bl':bl,
        'bg':bg,
        'bone':bone,
        'muscle':muscle,
    }
    print(context)
    return render(request, 'myapp/visual.html', context)


@login_required  # 限制只有登录了才能访问
def community(request):
    return render(request, 'myapp/community.html')


@login_required  # 限制只有登录了才能访问
def body(request, pindex=1):
    body_list = Body.objects.filter(user=request.user).order_by('-created_date')  # 使用过滤器筛选当前登录用户的数据
    p = Paginator(body_list, 6)  # 6条数据一页
    # 判断页码是否有效
    if pindex<1:
        pindex=1
    if pindex > p.num_pages:
        pindex = p.num_pages
    ulist = p.page(pindex)
    a, b, c = 1+6*(pindex-1), pindex*6, len(body_list)
    if b > c:
        b=c
    context = {'body_list': ulist, 'pindex':pindex, 'pagelist':p.page_range, 'a':a, 'b':b, 'c':c}
    return render(request, 'myapp/body.html', context)

# 'bmi', 'heart', 'ssy', 'szy', 'bl', 'bg', 'bone', 'muscle', 'diary'
@login_required   # 限制只有登录了才能访问
def detail(request, data_id):
    try:
        data = Body.objects.get(pk=data_id)
        print(data.bmi,data.heart,data.ssy,sep='\n')
    except Body.DoseNotExist:
        raise Http404('数据不存在')
    return render(request, 'myapp/body_detail.html', {'data': data})


@login_required  # 限制只有登录了才能访问
def result(request):
    import pandas as pd
    import joblib
    data = Prediction.objects.order_by('created_date')
    data = data[::-1][0]
    data = {
        '性别': [1 if data.gender == '男' else 0],
        '出生年份': [int(data.year)],
        '体重指数': [float(data.weight)/((float(data.tall)/100)**2)],
        '糖尿病家族史': [data.family],
        '舒张压': [float(data.press)],
        '口服耐糖量测试': [float(data.test)],
        '胰岛素释放实验': [float(data.release)],
        '肱三头肌皮褶厚度': [float(data.thick)],
            }
    data = pd.DataFrame(data)
    print(data)
    # ----------------特征工程----------------
    data['出生年份'] = 2023 - data['出生年份']  # 换成年龄
    # 体重指数正常值是在18.5-24之间,低于18.5是体重指数过轻.在24-27之间是体重超重.27以上考虑是肥胖.高于32了就是非常的肥胖。
    def BMI(a):
        if a < 18.5:
            return 0
        elif 18.5 <= a <= 24:
            return 1
        elif 24 < a <= 27:
            return 2
        elif 27 < a <= 32:
            return 3
        else:
            return 4
    data['BMI'] = data['体重指数'].apply(BMI)
    # 糖尿病家族史
    def FHOD(a):
        if a == '无记录':
            return 0
        elif a == '叔叔或者姑姑有一方患有糖尿病' or a == '叔叔或姑姑有一方患有糖尿病':
            return 1
        else:
            return 2

    data['糖尿病家族史'] = data['糖尿病家族史'].apply(FHOD)
    # 舒张压正常范围为60-90
    def DBP(a):
        if a < 60:
            return 0
        elif 60 <= a <= 90:
            return 1
        elif a > 90:
            return 2
        else:
            return a
    data['DBP'] = data['舒张压'].apply(DBP)
    # 加载模型
    model = joblib.load('myapp/static/tree.pkl')
    pre = model.predict(data)
    pre = pre[0]
    context = {'result': pre, 'BMI':data.iloc[0][2], 'press':data.iloc[0][4], 'test':data.iloc[0][5], 'release':data.iloc[0][6], 'thick':data.iloc[0][7] }
    print('预测结果',pre)

    return render(request, 'myapp/result.html', context)