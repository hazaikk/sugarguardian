from django.contrib.auth.models import User
from django.db import models
from django.utils.datetime_safe import datetime

# Create your models here.
Family = (('父母有一方患有糖尿病','父母有一方患有糖尿病'),('叔叔或者姑姑有一方患有糖尿病', '叔叔或者姑姑有一方患有糖尿病'), ('无记录','无记录'))


class Prediction(models.Model):
    applicant = models.ForeignKey(User, verbose_name='申请人', null=True, on_delete=models.SET_NULL)
    gender = models.CharField(max_length=4, verbose_name='性别')
    year = models.CharField(max_length=4, verbose_name='出生年份')
    tall = models.CharField(max_length=7, verbose_name='身高(cm)')
    weight = models.CharField(max_length=7, verbose_name='体重(kg)')
    family = models.CharField(max_length=25, verbose_name='糖尿病家族史', choices=Family,
                              help_text='父母有一方患有糖尿病、叔叔或者姑姑有一方患有糖尿病、无记录')
    press = models.CharField(max_length=7, verbose_name='舒张压(mmHg)')
    test = models.CharField(max_length=7, verbose_name='口服耐糖量测试(mmol/L)',
                            help_text='120分钟耐糖测试后的血糖值')
    release = models.CharField(max_length=7, verbose_name='胰岛素释放实验(pmol/L)',
                               help_text='服糖后120分钟的血浆胰岛素水平')
    thick = models.CharField(max_length=7, verbose_name='肱三头肌皮褶厚度(mm)',
                             help_text='在右上臂后面肩峰与鹰嘴连线的重点处，夹取与上肢长轴平行的皮褶，纵向测量')

    created_date = models.DateTimeField(verbose_name='创建日期', default=datetime.now)

    class Meta:
        verbose_name='样本'
        verbose_name_plural='糖尿病数据集'

# bmi heart ssy szy bl bg bone muscle diary
class Body(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', null=True, on_delete=models.SET_NULL)
    bmi = models.FloatField(max_length=7, verbose_name='体重指数',
                            help_text='正常范围：18.5 - 24.9')
    heart = models.FloatField(max_length=7, verbose_name='心率(次/分钟)',
                            help_text='正常范围：60 - 100 次/分钟')
    ssy = models.FloatField(max_length=7, verbose_name='收缩压(mmHg)',
                            help_text='正常范围：小于120 mmHg')
    szy = models.FloatField(max_length=7, verbose_name='舒张压(mmHg)',
                            help_text='正常范围：小于80 mmHg')
    bl = models.FloatField(max_length=7, verbose_name='总胆固醇(mg/dL)',
                            help_text='正常范围：小于200 mg/dL')
    bg = models.FloatField(max_length=7, verbose_name='血糖(mg/dL)',
                            help_text='正常范围：空腹血糖小于100 mg/dL')
    bone = models.FloatField(max_length=7, verbose_name='骨密度(T值)',
                            help_text='正常范围：T值大于-1')
    muscle = models.FloatField(max_length=7, verbose_name='肌肉质量(%)',
                            help_text='正常范围：男性为40-60%，女性为30-40%')

    diary = models.TextField(max_length=1024, blank=True, verbose_name='日记')
    created_date = models.DateTimeField(verbose_name='创建日期', default=datetime.now)

    class Meta:
        verbose_name='数据'
        verbose_name_plural='身体属性数据集'