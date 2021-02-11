from lib import wrangle, conversion


#--
path = './data/received_20210205.txt'
data = wrangle(path)

# print(data[0].keys())
# foo = conversion.make_array(data = data, field = 'time')
# foo = conversion.make_matrix(data = data, fields = ['time', 'laughs'])
# print(foo)
