import pickle

data = pickle.load(open('user_data.dat', 'rb'))
data['level'] = 0
write_file = open('user_data.dat', 'wb')
pickle.dump(data, write_file)
