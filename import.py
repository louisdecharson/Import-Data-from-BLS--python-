import requests
import json
import prettytable
headers = {'Content-type': 'application/json'} 
data = json.dumps({"seriesid": ['LNS11300000','SUUR0000SA0'],"startyear":"2011", "endyear":"2014"}) 
p = requests.post('http://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers) 
json_data = json.loads(p.text)
for series in json_data['Results']['series']:
    x=prettytable.PrettyTable(["series id","year","period","value","footnotes"])
    seriesId = series['seriesID']
    for item in series['data']:
        year = item['year']
        period = item['period']
        value = item['value']
        footnotes=""
        for footnote in item['footnotes']:
            if footnote:
                footnotes = footnotes + footnote['text'] + ','
        if 'M01' <= period <= 'M12':
            x.add_row([seriesId,year,period,value,footnotes[0:-1]])
    output = open("data"+seriesId+".txt","w")
    output.write (x.get_string())
    output.close()

# IMPORT PACKAGES
import requests
import json
from xlrd import open_workbook,cellname
from xlwt import Workbook


#### READ ####
data_bls=open_workbook('data_bls.xls')
sheet1 = book.sheet_by_index(0)
nb_rows=sheet1.nb_rows
nb_col=sheet1.nb_col
info=[]  #matrice qui contient les deux premiers rangs du fichier et renseignent sur 
#les séries et la dernière valeur

#On inscrit dans la matrice la liste des timeseries
row_index=1
col_index=0
compt_col=0
while col_index <= nb_col :
    info[row_index,compt_col]=str(sheet1.cell[row_index,col_index].value)
    col_index+=3
    compt_col+=1

row_index=1
col_index=0
compt_col=0

#### WRITE ####
data_bls = Workbook()
sheet1=data_bls.add_sheet('Sheet 1')

cur_col=0
headers = {'Content-type': 'application/json'} 
data = json.dumps({"seriesid": ['LNS11300000'],"startyear":"2011", "endyear":"2014"}) 
p = requests.post('http://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers) 
json_data = json.loads(p.text) 
for series in json_data['Results']['series']:
    cur_row=0
    seriesId = series['seriesID']
    row=sheet1.row(cur_row)
    row.write(cur_col,seriesId)
    for item in series['data']:
        year = item ['year']
        period = item['period']
        value = item['value']
        footnotes=""
        for footnote in item['footnotes']:
            if footnote:
                footnotes = footnotes + footnote['text'] + ','
        if 'M01' <= period <= 'M12':
            cur_row+=1
            row=sheet1.row(cur_row)
            row.write(cur_col,year)
            cur_col+=1
            row.write(cur_col,period)
            cur_col+=1
            row.write(cur_col,value)
            cur_col-=2
    cur_col+=3
data_bls.save('data_bls.xls')
