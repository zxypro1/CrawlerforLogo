import os

list = []
for parent, dir, names in os.walk('.\\lordicon'):
    if parent != '.\lordicon':
        for name in names:
            if name.split('.')[-1] == 'svg':
                list.append(parent + '\\' + name + '\n')

data = open('.//lordicon//data_list.txt', mode='w')
data.writelines(list)
