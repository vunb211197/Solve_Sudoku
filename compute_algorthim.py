import numpy as np

class Sudoku:
    def __init__(self,arr):
        self.arr = arr


    def find_empty_location(self,l):
        for row in np.arange(9):
            for col in np.arange(9):
                if(self.arr[row][col]==0):
                    l[0]=row
                    l[1]=col
                    return True
        return False

    #kiểm tra nếu trong hàng có trùng kí tự thì trả về True
    def used_in_row(self,row,num):
        for i in np.arange(9):   
            if(self.arr[row][i] == num):  
                return True
        return False

    #kiểm tra nếu trong cột có trùng kí tự thì trả về Tru
    def used_in_col(self,col,num):
        for i in np.arange(9):  
            if(self.arr[i][col] == num):  
                return True
        return False

    def check_box(self,a):
        rs = None
        if a%3 == 0 :
            rs =  [0,1,2]
        elif a%3 == 1 : 
            rs = [-1,0,1]
        else : 
            rs = [-2,-1,0]
        return rs

    # nếu trong ô 3*3 có cùng kí tự
    def used_in_box(self,row,col,num):
        for i in self.check_box(row) : 
            for j in self.check_box(col):
                if(self.arr[i+row][j+col] == num):     
                    return True 
        return False

    #kiểm tra thỏa mãn kí tự 
    def check_location_is_safe(self,row,col,num):
        # là phải thỏa mãn cả 3 cái này
        return not self.used_in_row(row,num) and not self.used_in_col(col,num) and not self.used_in_box(row - row%3,col - col%3,num)

    #giải soduku
    def solve_sudoku(self):
        l=[0,0] 
        #kiểm tra nếu ko có ô nào trống ( trả về false)
        if(not self.find_empty_location(l)):
            #thì trả về true
            return True 
        #còn nếu ko sẽ có l = [row,col] tương ứng với những ô chưa được điền ( có giá trị là  0)
        row=l[0]
        col=l[1] 
        #chạy num từ 1 đến 9
        for num in np.arange(1,10): 
            if(self.check_location_is_safe(row,col,num)): 
                self.arr[row][col]=num 
                #kiểm tra xem ok chưa 
                if(self.solve_sudoku()): 
                    return True 
                # failure, unmake & try again
                # nếu chưa thì làm lại 
                self.arr[row][col] = 0 
        
        return False

    def print_board(self):
        while(True):
            a = self.solve_sudoku()
            if a is True : 
                break
        print(self.arr)
        
