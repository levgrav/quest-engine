def change(data, index, value):
    item = data
    for i in range(len(index) - 1):
        item = item[index[i]]
    item[index[-1]] = value
