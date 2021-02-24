from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime,timedelta
from operator import itemgetter
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, draw, show


vc=pd.read_csv('../Data/VC-AFPs.csv',sep=",",float_precision='round_trip')
pd.options.display.float_format = '{:,.16f}'.format
columns=vc.columns
try:
    vc['FECHA']=pd.to_datetime(vc['FECHA'],format="%Y-%m-%d")
except:
    vc['FECHA']=pd.to_datetime(vc['FECHA'],format="%d/%m/%Y")
url="https://www.sbs.gob.pe/app/spp/variablesSPP_net/PagSS/variables_spp.aspx"
html=requests.get(url)
soup=BeautifulSoup(html.text,'html.parser')
tabla=soup.find_all('table',{'class':'APLI_tabla2'})
columnas=['FECHA']
for i in ['HAB','IN','PRO','PRI']:
    for j in ['CUO','AUM','VC']:
        for k in ['F0','F1','F2','F3']:
            columnas.append(i+"-"+j+"-"+k)

ubicaciones=[]
for i in [28,41,54,67]:
    aux=0
    for j in range(3):
        for k in range(4):
            if k==0:
                ubicaciones.append(i+aux)
            elif k==1:
                ubicaciones.append(i+aux-9)
            else:
                ubicaciones.append(ubicaciones[-1]+3)
        aux+=1

list_merge=[]
for rows in tabla:
    cells=rows.find_all("tr")
    list_merge.append([datetime.strptime(cells[0].text[-11:-1],"%d/%m/%Y").date()])

for j in ubicaciones:
    aux=0
    for rows in tabla:
        cells=rows.find_all("td")
        list_merge[aux].append(float(cells[j].text.strip().replace(',','')))
        aux+=1

list_merge=sorted(list_merge,key=itemgetter(0))
aux=0
while aux<len(list_merge)-1:
    if list_merge[aux][0]+timedelta(days=1)!=list_merge[aux+1][0]:
        list_merge.insert(aux+1,list_merge[aux].copy())
        list_merge[aux+1][0]=list_merge[aux+1][0]+timedelta(days=1)
    aux+=1
    
df_merge=pd.DataFrame(list_merge,columns=columnas)
df_merge['FECHA']=pd.to_datetime(df_merge['FECHA'],format="%Y-%m-%d")
final_df=vc.merge(df_merge,on=columnas,how='outer')
final_df.drop_duplicates(subset ="FECHA",keep = 'last', inplace = True) 
final_df
final_df.to_csv('../Data/VC-AFPs.csv',index=False)


################ Updating Charts ####################

sbs=final_df.copy()
del final_df

last_date=sbs['FECHA'].max()
last_date_last_year=datetime(last_date.year-1,12,31)

sbs_2=sbs[sbs.FECHA>=last_date_last_year].copy()
sbs_3=sbs_2.copy()

#Fondo 0

columns_f0=[i for i in sbs.columns if "VC-F0" in i]
columns_f0.insert(0,"FECHA")
for i in columns_f0[1:]:
    initial_value=sbs_2.loc[sbs_2.FECHA==last_date_last_year,i].values[0]
    sbs_3[i]=(sbs_2[i]/initial_value)*100

df0=sbs_3[columns_f0].copy()
df0.columns=['Date','Habitat','Integra','Prima','Profuturo']
df0=pd.melt(df0,'Date',var_name='Pension Funds',value_name='Value')

graph_f0 = plt.figure()
graph_f0.set_size_inches(12, 8);
graph_f0=sns.lineplot(x='Date',y='Value',hue='Pension Funds',data=df0)
graph_f0.set_title('Pension Funds Fondo 0 Return as of '+ last_date.strftime("%d/%m/%Y"),fontsize=20)
graph_f0.set_xlabel('Date',fontsize=15)
graph_f0.set_ylabel('YTD Return',fontsize=15)
plt.legend(fontsize='x-large', title_fontsize='40');
draw()

graph_f0.get_figure().savefig("../doc-source-images/returns_f0.png")
del graph_f0
#Fondo 1
columns_f1=[i for i in sbs.columns if "VC-F1" in i]
columns_f1.insert(0,"FECHA")

for i in columns_f1[1:]:
    initial_value=sbs_2.loc[sbs_2.FECHA==last_date_last_year,i].values[0]
    sbs_3[i]=(sbs_2[i]/initial_value)*100

df1=sbs_3[columns_f1].copy()
df1.columns=['Date','Habitat','Integra','Prima','Profuturo']
df1=pd.melt(df1,'Date',var_name='Pension Funds',value_name='Value')

graph_f1 = plt.figure()
graph_f1.set_size_inches(12, 8);
graph_f1=sns.lineplot(x='Date',y='Value',hue='Pension Funds',data=df1)
graph_f1.set_title('Pension Funds Fondo 1 Return as of '+ last_date.strftime("%d/%m/%Y"),fontsize=20)
graph_f1.set_xlabel('Date',fontsize=15)
graph_f1.set_ylabel('YTD Return',fontsize=15)
plt.legend(fontsize='x-large', title_fontsize='40');
draw()

graph_f1.get_figure().savefig("../doc-source-images/returns_f1.png")
del graph_f1
#Fondo 2

columns_f2=[i for i in sbs.columns if "VC-F2" in i]
columns_f2.insert(0,"FECHA")

for i in columns_f2[1:]:
    initial_value=sbs_2.loc[sbs_2.FECHA==last_date_last_year,i].values[0]
    sbs_3[i]=(sbs_2[i]/initial_value)*100

df2=sbs_3[columns_f2].copy()
df2.columns=['Date','Habitat','Integra','Prima','Profuturo']
df2=pd.melt(df2,'Date',var_name='Pension Funds',value_name='Value')

graph_f2 = plt.figure()
graph_f2.set_size_inches(12, 8);
graph_f2=sns.lineplot(x='Date',y='Value',hue='Pension Funds',data=df2)
graph_f2.set_title('Pension Funds Fondo 2 Return as of '+ last_date.strftime("%d/%m/%Y"),fontsize=20)
graph_f2.set_xlabel('Date',fontsize=15)
graph_f2.set_ylabel('YTD Return',fontsize=15)
plt.legend(fontsize='x-large', title_fontsize='40');
draw()
graph_f2.get_figure().savefig("../doc-source-images/returns_f2.png")
del graph_f2

#Fondo 3

columns_f3=[i for i in sbs.columns if "VC-F3" in i]
columns_f3.insert(0,"FECHA")

for i in columns_f3[1:]:
    initial_value=sbs_2.loc[sbs_2.FECHA==last_date_last_year,i].values[0]
    sbs_3[i]=(sbs_2[i]/initial_value)*100

df3=sbs_3[columns_f3].copy()
df3.columns=['Date','Habitat','Integra','Prima','Profuturo']
df3=pd.melt(df3,'Date',var_name='Pension Funds',value_name='Value')

graph_f3 = plt.figure()
graph_f3.set_size_inches(12, 8);
graph_f3=sns.lineplot(x='Date',y='Value',hue='Pension Funds',data=df3)
graph_f3.set_title('Pension Funds Fondo 3 Return as of '+ last_date.strftime("%d/%m/%Y"),fontsize=20)
graph_f3.set_xlabel('Date',fontsize=15)
graph_f3.set_ylabel('YTD Return',fontsize=15)
plt.legend(fontsize='x-large', title_fontsize='40');
draw()
graph_f3.get_figure().savefig("../doc-source-images/returns_f3.png")
del graph_f3

