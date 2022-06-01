from django import forms


class BootStrap:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加class = "form-control"
        for name, field in self.fields.items():
            # if name == "password":#只有password不加样式
            #     continue
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label


            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label
                }


class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass


class BootStrapForm(BootStrap,forms.Form):
    pass

    # 验证有效性方法二
    # def clean_num(self):
    #     txt_num = self.cleaned_data["num"]
    #
    #     exists = models.PrettyNum.objects.filter(num=txt_num).exists()
    #     if exists:
    #         raise ValidationError("钩子验证，手机号已存在")
    #
    #     # 验证通过，用户输入的值返回
    #     return txt_num