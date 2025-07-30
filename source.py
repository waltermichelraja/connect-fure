#bai i think we could go with matrix first then we alter it
#stack class
class Stack:
    def __init__(self):
        self.stack=[]
    def push(self, c):
        self.stack.append(c)
    def pop(self):
        self.stack.pop()
    def peek(self):
        return self.stack[-1]
        
s=Stack() #dont worry used to test the snipet can delete it later
s.push(5)
print(s.stack)

#also now i am not creating user,board classes jst logic
class board:
    def __init__(self):
        self.board=[]
        for i in range(8):
            ss=Stack()
            self.board.append(ss)
    
#i dont know how to format stuffs you do it
def flowcheck(bo, pl):
    if i==1:  
        bo.board[pl-1].push(2)
    else:
        bo.board[pl-1].push(3)
    while bo.board[pl-1]:
        c=1
        bo.board[pl-1].peak() #bro i stop here i am goin to sleep

i=1
b=board()
while True:
    if i==1:
        p=int(input("enter"))
        flowcheck(b, p)
        i+=1
    else:
        p1=int(input("enter"))
        flowcheck(b, p1)
        i-=1
     

