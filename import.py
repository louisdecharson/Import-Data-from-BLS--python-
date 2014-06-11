import requests
import json
import prettytable
import xlrd
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
