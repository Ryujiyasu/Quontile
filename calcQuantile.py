import itertools
import statistics

seq = [57,59,60,100,80,58,57,58,300,61,62,60,62,110,57,130,45,65,78,12]

list_item = list(itertools.combinations(seq,10))
list_quantile=[]
list=[]
center=[]

for item in list_item:
    q=statistics.quantiles(item, n=4)
    if q[1] > 60:
        list_quantile.append(q[2]-q[0])
        list.append(item)
        center.append(q[1])
    else:
        pass

min_index=list_quantile.index(min(list_quantile))
max_index=list_quantile.index(max(list_quantile))
print(center[max_index])
print(list[max_index])
print(max(list_quantile))
print(center[min_index])
print(list[min_index])
print(min(list_quantile))