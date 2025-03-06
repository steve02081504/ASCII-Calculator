from os import name
if name == 'nt':
    print("当前操作系统为windows")
    txt = input() + '\r\n'  
elif name == 'posix':
    print("当前操作系统为:Unix/Linux/MacOS")
    txt = input() + '\n'  
else:
    print("当前操作系统为:未知系统系统,使用类Unix风格换行符")
    txt = input() + '\n'  
print("输入字符为:", txt)
sum = 0                     
for character in txt:
    sum += ord(character)
print("ASCII之和为:", sum)
