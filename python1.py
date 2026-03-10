import pickle
def write():
    with open ("student1.dat","ab")as obj:
        rno=int(input("Enter rollno"))
        subject=input("Enter subject")
        s=[rno, subject]
        pickle.dump(s,obj)
               
def read():
    found=0
    with open ("student1.dat","rb")as obj:          
        while True:
            try:
                s1=pickle.load(obj)
                print(s1)
                found=1
            except EOFError:
                break
        if found==0:
            print("File is empty")

def search(x):
    found=0
    with open ("student1.dat","rb")as obj:
        while True:
            try:
                s1=pickle.load(obj)
                if s1[0]==x:
                    print(s1)
                    found=1
                    break
            except EOFError:
                print("Record not found")
                break
        



#write()
#write()
#write()
read()
rol_no = int(input("enter your roll-no: "))
search(rol_no)