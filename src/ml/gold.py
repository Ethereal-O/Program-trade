
import csv
import torch
from torch import nn
import os
path1="LBMA-GOLD.csv"
path2="BCHAIN-MKPRU.csv"
def readData(path):
    price=[]
    with open(path, 'r', encoding="utf-8") as f:
        gtReader = csv.reader(f, delimiter=';')  # csv parser for annotations file
        next(gtReader)  # skip header
        # loop over all images in current annotations file
        for row in gtReader:
            if ','.join(row).split(',')[1]=="":
                continue
            else:
                price.append(float(','.join(row).split(',')[1]))

    return price


price=readData(path1)
print("加载的文件路径为：",os.getcwd()+"\\"+path1)
def predict(t_start,t_end,preprice,seq=15):
    assert seq<=t_end-t_start
    global price
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #t_start -- t_end 拿来训练，seq是能用来推测的长度，推测t_end+1天的数据
    li_x = []
    li_y = []
    train_price=preprice[t_start:t_end]#切片切到t_end-1，对应t_end天
    maxv=max(train_price)
    minv=min(train_price)
    #归一化
    for i in range(len(train_price)):
        train_price[i]=(train_price[i]-minv)/(maxv-minv)

    # 因为数据集较少，序列长度太长会影响结果
    for i in range(len(train_price) - seq):
        li_x.append(train_price[i: i + seq])
        li_y.append(train_price[i + seq])

    train_x = (torch.tensor(li_x).float()).reshape(-1, seq, 1).to(device)
    train_y = (torch.tensor(li_y).float()).reshape(-1, 1).to(device)

    eval=(torch.tensor(li_x[-1]).float()).reshape(-1, seq, 1).to(device)

    class Net(nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            self.lstm = nn.LSTM(input_size=1, hidden_size=32, num_layers=1, batch_first=True)
            for name, param in self.lstm.named_parameters():
                nn.init.normal_(param, 0, 1)#正交初始化
            # 输入格式是1，输出隐藏层大小是32，对于序列比较短的数据num_layers不要设置大，否则效果会变差
            # 原来的输入格式是：(seq, batch, shape)，设置batch_first=True以后，输入格式就可以改为：(batch, seq, shape)，更符合平常使用的习惯
            self.linear = nn.Linear(32 * seq, 1)
            nn.init.xavier_normal_(self.linear.weight)
            nn.init.constant_(self.linear.bias, 0)
        def forward(self, x):
            x, (h, c) = self.lstm(x)
            x = x.reshape(-1, 32 * seq)
            x = self.linear(x)
            return x


    model = Net().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.003)

    loss_fun = nn.MSELoss()

    model.train()
    for epoch in range(1500):
        output = model(train_x)
        loss = loss_fun(output, train_y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    model.eval()
    pre=model(eval).data.reshape(-1).cpu().item()* (maxv-minv)+minv
    return pre,'%.3f' % (abs(pre-price[t_end])/price[t_end]*100)+"%"

def pre_t(t_start,t_end,t_futrue,seq=15):
    pre_price=price[:]#浅拷贝
    pre_list=[]
    wc_list=[]
    for i in range(t_futrue):
        pre,wucha=predict(t_start,t_end+i,pre_price,seq)
        pre_price[t_end+i]=pre
        pre_list.append(pre)
        wc_list.append(wucha)
    return pre_list,wc_list


with open('LBMA-GOLD-1.csv', 'w', encoding='UTF8',newline="") as f:
    writer = csv.writer(f)
    for i in range(8,16):
        a, b = pre_t(0, i, 5,seq=i-1)
        data = [i] + a + b
        writer.writerow(data)
        print("第", i, "天时预测后5天数据为：", a, '\n\t\t\t\t\t\t', price[i:i + 5], '\n\t\t\t\t\t\t', b)
    for i in range(16,len(price)-4):
        a,b=pre_t(0,i,5)
        data=[i]+a+b
        writer.writerow(data)
        print("第",i,"天时预测后5天数据为：",a,'\n\t\t\t\t\t\t',price[i:i+5],'\n\t\t\t\t\t\t',b)
    for i in range(len(price)-4,len(price)):
        a,b=pre_t(0,i,len(price)-i)
        data=[i]+a+b
        writer.writerow(data)
        print("第",i,"天时预测后",len(price)-i,"天数据为：",a,'\n\t\t\t\t\t\t',b)
