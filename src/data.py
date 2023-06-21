c:\Users\wuzij\Desktop\wuzij\programtrading\program-trade\Program-trade\venv-quant\Scripts\python.exeimport tushare as ts
import pandas as pd
token ='5c4acae8b06093f399f1431c30f95be5f202f11125fc297eef691e01'
pro= ts.pro_api()
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
data=data['ts_code']
for i in list(stocks):
    data1 = ts.pro_bar(ts_code=i,start_date='20100101',end_date='20210527', adj='qfq')
    data=data1[['trade_date','open','high','low','close','vol']]
    data.index = pd.to_datetime(data.trade_date)
    data = data.sort_index()
    print(data)
    break
