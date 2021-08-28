import requests
import json
import pandas as pd
from LineNotify import lineNotifyMessage
import datetime

headers = {
    'content-type': 'text/html; charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

# -------------  每日殖利率9.8%以上 -------------------
# 上市
def earning_ratio_ex(begin,rank=None):
    '''
    :param begin:  20201112
    :param rank: number
    https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=json&date=20210401&selectType=ALL&_=1617593935013

    '''
    print(begin)
    dividend = requests.get('https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=json&date={}&selectType=&_=1628401659564'.format(begin)).content
    data = json.loads(dividend)
    number = 0
    setting = 0
    select_data = []
    #print(datetime.datetime.now().year -1912)  #去年股利
    for i, index in enumerate(data['data']):
        if index[3] == (datetime.datetime.now().year -1912):
            select_data.append(index)
    #print(select_data)
    for i, index in enumerate(select_data):
        if float(index[2]) >= 9.8:
            number += 1
    # print(number)
    if rank is None:
        if number != 0:
            rank = number
        else:
            rank = 1
    else:
        setting += 1
    title = ['證券代號', '證券名稱', 'yieldR', '股利年度', '本益比', '股價淨值比', '財報年/季']
    df = pd.DataFrame(select_data, columns=title) #data['fields']
    # new_df.assign(total=new_df.total.astype(int)).sort_values(by='total', ascending=False, inplace=False)
    df = df.assign(yieldR=df.yieldR.astype(float)).sort_values(by='yieldR', ascending=False).iloc[:rank]
    df.columns = data['fields']
    print(df)
    msg = '\n'
    for num in range(rank):
        for i, j in zip(df.iloc[num].index.tolist(), df.iloc[num].tolist()):
            #print(i, j)
            msg = msg + str(i) + ':' + str(j) + '\n'
        msg = msg + '---------------\n'
    #print(msg)
    if setting == 0:
        lineNotifyMessage('\n{}\n上市殖利率>=10%，共{}檔\n---------------'.format(begin, rank) + msg)
    else:
        lineNotifyMessage('\n{}\n上市殖利率排名前{}名\n---------------'.format(begin, rank) + msg)
    df.to_csv('earning_ratio_exchange_{}.csv'.format(begin), index=False)

#earning_ratio_ex(20210401)

def earning_ratio_cou(begin, rank = None):
    '''
    https://www.tpex.org.tw/web/stock/aftertrading/peratio_analysis/pera_result.php?l=zh-tw&d=109/11/18&c=&_=1605844331685
    :param begin:  20201112
    :param rank: number
    '''
    dividend = requests.get('https://www.tpex.org.tw/web/stock/aftertrading/peratio_analysis/pera_result.php?l=zh-tw&d={}&c=&_=1617558954523'.format(begin)).content
    data = json.loads(dividend)
    #print(data)
    hd = ['股票代號', '名稱', '本益比', '每股股利', '股利年度', 'yieldR', '股價淨值比']
    hd1 = ['股票代號', '名稱', '本益比', '每股股利', '股利年度', '殖利率(%)', '股價淨值比']


    number = 0
    setting = 0 #判斷是否有輸入選取數量
    select_data = []
    #print(datetime.datetime.now().year -1912)  #去年股利
    for i, index in enumerate(data['aaData']):
        if int(index[4]) == (datetime.datetime.now().year -1912):
            select_data.append(index)
    # print(select_data)

    for i, index in enumerate(select_data):
        if float(index[5]) >= 9.8:
            number += 1
    # print(number)
    if rank is None:
        if number != 0:
            rank = number
        else:
            rank = 1
    else:
        setting += 1
    df = pd.DataFrame(select_data, columns=hd)
    df = df.assign(yieldR=df.yieldR.astype(float)).sort_values(by='yieldR', ascending=False).iloc[:rank]
    df.columns = hd1
    #print(df)
    # print(begin.replace('/', ''))
    msg = '\n'
    for num in range(rank):
        for i, j in zip(df.iloc[num].index.tolist(), df.iloc[num].tolist()):
            #print(i, j)
            msg = msg + str(i) + ':' + str(j) + '\n'
        msg = msg + '---------------\n'
    print(msg)
    if setting == 0:
        lineNotifyMessage('\n{}\n上櫃殖利率>=10%，共{}檔\n---------------'.format(begin, rank) + msg)
    else:
        lineNotifyMessage('\n{}\n上櫃殖利率排名前{}名\n---------------'.format(begin, rank) + msg)
    df.to_csv('earning_ratio_counter_{}.csv'.format(begin.replace('/', '')), index=False)

# earning_ratio_cou('110/04/01')

#民國轉西元年函式
def transfer_date(date):
    y = str(date)[0:4]
    m = str(date)[4:6]
    d = str(date)[6:8]
    return str(int(y) - 1911) + '/' + m + '/' + d

yieldRate = ['earning_ratio_ex', 'earning_ratio_cou']

def yieldData(begin=None, rank=None):   #日期格式:西元年月日
    if begin is None:
        dt = datetime.datetime.now().date()  # datetime(2021,4,4)

        if dt.weekday() == 6:
            dt = dt - datetime.timedelta(2)
        elif dt.weekday() == 5:
            dt = dt - datetime.timedelta(1)

        if dt.month < 10:
            month = '0' + str(dt.month)
        else:
            month = str(dt.month)
        if dt.day < 10:
            day = '0' + str(dt.day)
        else:
            day = str(dt.day)

        begin = str(dt.year) + month + day
        print(begin)

    for i in yieldRate:
        if i == 'earning_ratio_ex':
            earning_ratio_ex(begin, rank)
        elif i == 'earning_ratio_cou':
            earning_ratio_cou(transfer_date(begin), rank)


# -------------  每日殖利率9.8%以上 -------------------
yieldData('20210813')
