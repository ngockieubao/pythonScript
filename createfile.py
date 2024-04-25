import os

print("Hello There, this is python script!")
os.chdir("C:/Users/Admin/Desktop/")

for i in range(0,3):
    i=i+1
    f=open(f"test{i}.txt", "x")
    f.write(f"This is test file {i}.")
    print(f"File {i} is created.")
    f.close()
print("Program is finished!")