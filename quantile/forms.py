from django import forms

LIBRARIES_CHOICES = (
    ("","-----"),
    ('high','以上'),
    ('low','以下'),
)



class QuantileForm(forms.Form):
    file = forms.FileField(label='ファイル',required=True)
    number = forms.IntegerField(
    label="組み合わせ数",
    required = True,
    )
    base = forms.IntegerField(
    label="値",
    required = True,
    )
    choice1 = forms.ChoiceField(
    label="選択",
    widget = forms.Select,
    choices = LIBRARIES_CHOICES,
    required = True,
    )
    choice2 = forms.ChoiceField(
        label="選択3",
        widget=forms.Select,
        choices=(
            ('non', '------'),
            ('cen', '中央値'),
            ('avr', '平均値'),
        ),
        required=True,
    )
    base2 = forms.IntegerField(
    label="値",
    required = True,
    )
    choice3 = forms.ChoiceField(
    label="選択",
    widget = forms.Select,
    choices = LIBRARIES_CHOICES,
    required = True,
    )
    choice4 = forms.ChoiceField(
    label="選択",
    widget = forms.Select,
        choices=(
            ('max', '四分位範囲最大を求める'),
            ('min', '四分位範囲最小を求める'),
        ),
    required = True,
    )