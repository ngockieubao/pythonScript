import os
from os import system

print("Hi, this is script get server information.")
print("\n=========================================================================")
os.chdir("/home")
f=open(f"server-info.txt", "x")
system("cat /proc/cpuinfo | grep 'model name' || free -m || df -h > server-info.txt")
f.write()
f.close()
print("\n=========================================================================")
print("Program is finished!")