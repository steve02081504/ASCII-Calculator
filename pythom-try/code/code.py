from os import name
if name == 'nt':
    txt = input() + '\r\n'  
elif name == 'posix':
    txt = input() + '\n'  
else:
    txt = input() + '\n'  
sum = 0                     
for character in txt:
    sum += ord(character)
print(sum)
