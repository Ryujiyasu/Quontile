from django.shortcuts import render
import itertools
import statistics
from .forms import QuantileForm
# Create your views here.
import pandas as pd
from django.shortcuts import redirect
import datetime
import numpy as np

def calculate(file,number,base,choice1,choice2,base2,choice3):
    df= pd.read_excel(file)
    df = df[5:]
    i=df[df["Range Overview"].isnull()].index[0]
    df =  df[:i-5]
    df=df.set_index("Range Overview")
    df_data = df[1:]
    df_data.columns=df.iloc[0,].values
    df_output=pd.DataFrame()

    number_list = np.array(df_data['Average'].str.replace("%", "").astype("float16"))
    company_list=np.array(df_data['Average'].index)
    dictionary = dict(zip(number_list, company_list))
    print(number_list)

    list_item = itertools.combinations(number_list, int(number))
    list_quantile = []
    list = []
    center = []
    for item in list_item:
        flg1=False
        flg2=False
        q = statistics.quantiles(item, n=4)
        if (q[2] - q[0])>=float(base) and choice1 == "high":
            flg1=True
        elif (q[2] - q[0])<=float(base) and choice1=="low":
            flg1 = True
        if choice2=="cen" and q[1] >= float(base2) and choice3 == "high":
            flg2=True
        elif choice2=="cen" and q[1] <= float(base2) and choice3 == "low":
            flg2 = True
        elif choice2 == "avr" and np.average(q) >= float(base2) and choice3 == "high":
            flg2 = True
        elif choice2 == "avr" and np.average(q) <= float(base2) and choice3 == "low":
            flg2 = True
        if flg1 and flg2:
            list_quantile.append(q[2] - q[0])
            list.append(item)
            center.append(q[1])

    min_index = list_quantile.index(min(list_quantile))
    max_index = list_quantile.index(max(list_quantile))
    max_company=[]
    min_company = []
    for item in list[max_index]:
        max_company.append(dictionary[item])
    for item in list[min_index]:
        min_company.append(dictionary[item])

    df_tempdata=pd.DataFrame({"四分位幅最大のCompany名":max_company,
        "四分位幅最大の組み合わせ":list[max_index],
        "四分位幅最大値":max(list_quantile),
        "四分位幅最大の組み合わせの中央値": center[min_index],
        "": "",
        "四分位幅最小のCompany名": min_company,
        "四分位幅最小の組み合わせ":list[min_index],
        "四分位幅最小値":min(list_quantile),
        "四分位幅最小の組み合わせの中央値":center[min_index]
    })
    df_tempdata["四分位幅最大値"][1:]=""
    df_tempdata["四分位幅最大の組み合わせの中央値"][1:] = ""
    df_tempdata["四分位幅最小値"][1:] = ""
    df_tempdata["四分位幅最小の組み合わせの中央値"][1:] = ""
    df_output=pd.concat([df_output,df_tempdata],axis=1)
    file_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    data_name="media/" + file_name + "_output.xlsx"
    df_output.to_excel(data_name)

    return data_name



def index(requsts):
    number=""
    form=QuantileForm()
    if requsts.method=="POST":
        data_name=calculate(requsts.FILES['file'],requsts.POST["number"],
                            requsts.POST["base"],requsts.POST["choice1"],
                            requsts.POST["choice2"],requsts.POST["base2"],
                            requsts.POST["choice3"])

        return redirect(data_name)
    params={
        'form':form,
        "num":number,
    }
    return render(requsts,'quantile/index.html',params)



