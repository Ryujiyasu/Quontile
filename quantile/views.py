from django.shortcuts import render
import itertools
import statistics
from .forms import QuantileForm
import pandas as pd
from django.shortcuts import redirect
import datetime
import numpy as np

def calculate(file,number,base,choice1,choice2,base2,choice3,choice4):
    df= pd.read_excel(file)
    df = df[5:]
    i=df[df["Range Overview"].isnull()].index[0]
    df =  df[:i-5]

    df_2=df.set_index("Range Overview")



    df_data = df_2[1:]
    df_data.columns=df_2.iloc[0,].values



    df_data_2=df[1:]
    df_data_2.columns = df.iloc[0,].values


    df_output=pd.DataFrame()
    df_columns = df_data.columns



    number_list = np.array(df_data[df_columns[-1]].str.replace("%", "").astype("float16"))
    company_list=np.array(df_data[df_columns[-1]].index)
    dictionary = dict(zip(number_list, company_list))

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

    if choice4=="max":
        max_index = list_quantile.index(max(list_quantile))
        max_company = []
        for item in list[max_index]:
            max_company.append(dictionary[item])
        df_tempdata=pd.DataFrame({"Comparable Taxpayer":max_company,
            "四分位幅最大の組み合わせ":list[max_index],
            "四分位幅最大値":max(list_quantile),
            "四分位幅最大の組み合わせの中央値": center[max_index],
        })
        df_tempdata["四分位幅最大値"][1:]=""
        df_tempdata["四分位幅最大の組み合わせの中央値"][1:] = ""
    else:
        min_index = list_quantile.index(min(list_quantile))
        min_company = []
        for item in list[min_index]:
            min_company.append(dictionary[item])
        df_tempdata = pd.DataFrame({"Comparable Taxpayer": min_company,
                                    "四分位幅最小の組み合わせ": list[min_index],
                                    "四分位幅最小値": min(list_quantile),
                                    "四分位幅最小の組み合わせの中央値": center[min_index],
                                    })
        df_tempdata["四分位幅最小値"][1:] = ""
        df_tempdata["四分位幅最小の組み合わせの中央値"][1:] = ""

    df_tempdata=pd.merge(df_tempdata,df_data_2,on="Comparable Taxpayer")
    df_tempdata = df_tempdata.set_index("Comparable Taxpayer")
    df_tempdata.loc['Minimum'] = ""
    df_tempdata.loc['Lower Quartile'] = ""
    df_tempdata.loc['Median'] = ""
    df_tempdata.loc['Mean'] = ""
    df_tempdata.loc['Upper Quartile'] = ""
    df_tempdata.loc['Maximum'] = ""
    for i in range(len(df_tempdata.columns)-3):
        list=[]
        for k in df_tempdata.iloc[:,3+i]:
            try:
                list.append(float(k.replace("%", "")))
            except:
                pass
        print(list)
        list=np.array(list)

        df_tempdata.loc["Minimum",df_tempdata.iloc[:,3+i].name]=str(list.min())+"%"
        if len(list) >= 7:
            q = statistics.quantiles(list, n=4)
            df_tempdata.loc["Lower Quartile", df_tempdata.iloc[:, 3 + i].name] = str(q[0]) + "%"
            df_tempdata.loc["Median", df_tempdata.iloc[:, 3 + i].name] = str(q[1]) + "%"
            df_tempdata.loc["Upper Quartile", df_tempdata.iloc[:, 3 + i].name] = str(q[2]) + "%"
        df_tempdata.loc["Mean", df_tempdata.iloc[:, 3 + i].name] = str(round(list.mean(),2)) + "%"
        df_tempdata.loc["Maximum", df_tempdata.iloc[:, 3 + i].name] = str(list.max()) + "%"

    file_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    data_name="media/" + file_name + "_output.xlsx"
    df_tempdata.to_excel(data_name)

    return data_name



def index(requsts):
    number=""
    form=QuantileForm()
    if requsts.method=="POST":
        data_name=calculate(requsts.FILES['file'],requsts.POST["number"],
                            requsts.POST["base"],requsts.POST["choice1"],
                            requsts.POST["choice2"],requsts.POST["base2"],
                            requsts.POST["choice3"],requsts.POST["choice4"])

        return redirect(data_name)
    params={
        'form':form,
        "num":number,
    }
    return render(requsts,'quantile/index.html',params)



