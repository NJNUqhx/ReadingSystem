from reading_system import models
from reading_system.utils.bootstrap import BootStrapModelForm
from django.core.exceptions import ValidationError


class StuModelForm(BootStrapModelForm):
    class Meta:
        model = models.StuExactInfo
        fields = ["name", "age", "grade", "account", "password", "admintec", ]

    def clean_account(self):
        txt_account = "njnu" + str(models.StuExactInfo.objects.count() + 1000)
        exists = models.StuExactInfo.objects.filter(account=txt_account).exists()
        if exists:
            raise ValidationError("已存在该学生账号")
        return txt_account


class StuEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.StuExactInfo
        fields = ["name", "age", "grade", "password", "admintec"]

    def clean_account(self):
        txt_account = self.cleaned_data["account"]
        exists = models.StuExactInfo.objects.exclude(id=self.instance.pk).filter(account=txt_account).exists()
        if exists:
            raise ValidationError("已存在该学生账号")
        return txt_account


class StuTestInfo(BootStrapModelForm):
    class Meta:
        model = models.StuTestInfo
        fields = "__all__"
