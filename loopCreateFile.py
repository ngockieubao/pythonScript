import os

print("This script file to create more & more file for test hardware without internet.")

i=1
while True:
    f=open("test%i"%i,"w")
    f.write("This is test file %i"%i)
    f.close()
    print("File %i is created."%i)
    i=i+1
