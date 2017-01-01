import pickle

file_name = input('Name: ')

read_file = open(file_name + '.txt', 'r')
info = eval(read_file.read())

write_file = open(file_name + '.dat', 'wb')
pickle.dump(info, write_file)

write_file.close()
read_file.close()
