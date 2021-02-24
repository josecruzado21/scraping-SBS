from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime,timedelta
from operator import itemgetter
vc=pd.read_csv('VC-AFPs.csv',sep=",",float_precision='round_trip')
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
final_df.to_csv('VC-AFPs.csv',index=False)
