# Easy Matrices!
# Gustavo Angulo 15-112 F15 Term Project
# AndrewID: gangulo
# 112 Section D


import numpy as np
from numpy.linalg import *
from tkinter import *
import copy
import random


# Numpy downloaded from http://www.numpy.org/


class Matrix(object):
    def __init__(self,values,x,y,history=None,locked=False):
        #creates a matrix object
        # x,y is the top left corner of the matrix
        # if locked = True, size and values can't be changed
        self.values = roundList(values)
        self.color = "black"
        self.x = x
        self.y = y
        self.locked = locked
        #contains tuples in the form (row,col) with the color for the highlight
        self.highlightedValues = []
        # contains history of how matrix was made, None if user makes it
        # operation in index 0 of list, objects in index 1-2
        self.history = history


    def draw(self,canvas):
        # draws matrix object 
        cellColor = "white" # cell backgrounds are default white
        margin = 10 # space between number and bracket
        numberSepX = 20 # space between numbers side by side
        numberSepY = 15 # space between numbers vertically
        numberWidth = getNumberWidth(self.values)  # largest number width
        # draws brackets around numbers
        drawBrackets(self,canvas,margin,numberSepX,numberSepY,numberWidth)
        for row in range(len(self.values)):
            for col in range(len(self.values[0])):
                # x, y is top left corner of cell
                x = self.x + margin + numberSepX*col + numberWidth*col
                y = self.y + margin + numberSepY*row + numberSepY*row
                if (row,col) in self.highlightedValues: 
                    # changes cell color to yellow if number is highlighted
                    cellColor = "yellow"
                canvas.create_rectangle(x,y,x+numberWidth,y+numberSepY,
                    fill=cellColor, width=0)
                canvas.create_text(x,y,text=str(self.values[row][col]),
                    fill=self.color,anchor=NW, font="Times 20")
                # resets cell color back to white
                cellColor = "white"
    

    def drawDash(self,canvas):
        # draws a dashed rectangle around matrix to indicate selection
        gap = 20 # space between dash and matrix
        margin = 10 # space between number and bracket
        numberSepX = 20 # space between numbers side by side
        numberSepY = 15 # space between numbers vertically
        numberWidth = getNumberWidth(self.values)  # largest number width
        rows = len(self.values)
        cols = len(self.values[0])
        x0,y0 = self.x - gap, self.y - gap
        x1 = x0 + margin*2 + numberWidth*cols + numberSepX*(cols-1) + gap*2
        y1 = y0 + margin*2 + numberSepY*rows + numberSepY*(rows-1) + gap*2
        width= 3 # line width and dash separation
        canvas.create_line(x0,y0,x1,y0,width=width,dash=(width,width))
        canvas.create_line(x1,y0,x1,y1,width=width,dash=(width,width))
        canvas.create_line(x1,y1,x0,y1,width=width,dash=(width,width))
        canvas.create_line(x0,y1,x0,y0,width=width,dash=(width,width))


    def matrixContainsClick(self,x,y):
        # returns true if user's click is inside the matrix self
        margin = 10 # space between number and bracket
        numberSepX = 20 # space between numbers side by side
        numberSepY = 15 # space between numbers vertically
        numberWidth = getNumberWidth(self.values)  # largest number width
        rows = len(self.values) + 1
        cols = len(self.values[0]) + 1
        x0,y0 = self.x, self.y
        x1 = x0 + margin + numberWidth*cols + numberSepX*cols
        y1 = y0 + margin + numberWidth*rows + numberSepY*rows
        if x > x0 and x < x1 and y > y0 and y<y1:
            return True
        else:
            return False

    def findInverse(self,data):
        # creates an instance of matrix object that is self's inverse
        try:
            result = inv(self.values)
            # converts from numpy array to 2d list
            result = list(result)
            for row in range(len(result)):
                result[row] = list(result[row])
            # x,y is right of original matrix
            matrixSep = 60
            x,y = self.x + len(self.values[0])*matrixSep, self.y
            history = ["-1", self]
            data.matrices.append(Matrix(result,x,y,history))
        except: # matrix can't be inverted
            self.color = "red"

    def solveSystem(self,data):
        # creates an instance of Matrix with solution to the system of self
        # self is assumed to be an augmented matrix, where the last col
        # are the solutions to the linear equations
        def solve(L):
            lastCol = len(L[0]) - 1 # index of last column
            result = [] # matrix cosisting of last columns
            for row in L:
                result.append([row[lastCol]])
                row.pop(lastCol)
            return(np.linalg.solve(L,result))
        try:
            self.color = "black" # resets color to black
            # x,y is right of original matrix
            matrixSep = 60
            x,y = self.x + len(self.values[0])*matrixSep, self.y
            result = solve(copy.deepcopy(self.values))
            # converts from numpy array to 2d list
            result = list(result)
            for row in range(len(result)):
                result[row] = list(result[row])
            data.matrices.append(Matrix(result,x,y))
        except: # matrix has no solution
            self.color = "red"

    def transpose(self,data):
        # creates an instance of matrix that is the transpose of matrix self
        rows, cols = len(self.values), len(self.values[0])
        result = make2dList(cols,rows)
        for row in range(len(self.values)):
            for col in range(len(self.values[0])):
                result[col][row] = self.values[row][col]
        # x,y is right of original matrix
        matrixSep = 60
        x,y = self.x + len(self.values[0])*matrixSep, self.y
        history = ["T",self]
        data.matrices.append(Matrix(result,x,y,history))

    def findDeterminant(self,data):
        # creates an instance of Number with the determinant of self
        try:
            self.color = "black" # resets color to black
            matrixSepX,matrixSepY = 50,20
            x,y = self.x - matrixSepX, self.y + matrixSepY # left of the matrix
            determinant = int(np.linalg.det(self.values))
            history = ["det",self]
            data.numbers.append(Number(determinant,x,y,history))
        except:
            # matrix is not square
            self.color = "red"


    def square(self,data):
        # creates an instance of matrix object that is self raised to nth power
        result = np.linalg.matrix_power(self.values,2)
        # converts from numpy array to 2d list
        result = list(result)
        for row in range(len(result)):
            result[row] = list(result[row])
        # x,y is center
        x,y = data.width/2, data.height/2
        history = ["2", self]
        data.matrices.append(Matrix(result,x,y,history))

    def addRow(self):
        # adds row of 1's to matrix
        cols = len(self.values[0])
        self.values.append([1]*cols)
        # clears history because matrix has changed
        self.history = None

    def addCol(self):
        # adds column of 1's to matrix
        for row in range(len(self.values)):
            self.values[row].append(1)
        # clears history because matrix has changed
        self.history = None

    def deleteRow(self):
        # deletes last row from matrix
        if len(self.values) > 1:
            self.values.pop()
        # clears history because matrix has changed
        self.history = None

    def deleteCol(self):
        # deletes last col from matrix
        if len(self.values[0]) > 1:
            for row in range(len(self.values)):
                self.values[row].pop()
        # clears history because matrix has changed
        self.history = None



class Number(object): 
    # number objects, used for scalar multiplication and exponents
    def __init__(self,value,x,y,history=None,locked=False):
        self.value = value
        # x,y is top left corner of number
        self.x = x
        self.y = y
        self.locked = locked
        self.history = history

    def draw(self,canvas):
        # draws number object
        canvas.create_text(self.x,self.y,text=str(self.value),
                        anchor=NW, font="Times 40")

    def numberContainsClick(self,x,y):
        # returns true if user clicks on object
        fontSize = 40
        numberSize = len(str(self.value)) * fontSize
        x0,y0 = self.x, self.y
        x1 = x0 + numberSize
        y1 = y0 + numberSize
        if x > x0 and x < x1 and y > y0 and y<y1:
            return True
        else:
            return False

    def drawDash(self,canvas):
        # draws a dashed rectangle around number
        gap = 10
        fontSize = 20
        numberWidth = len(str(self.value)) * fontSize
        numberHeight = 40
        x0,y0 = self.x - gap, self.y-gap
        x1 = x0 + numberWidth + gap*2
        y1 = y0 + numberHeight + gap*2
        width = 3
        canvas.create_line(x0,y0,x1,y0,width=width,dash=(width,width))
        canvas.create_line(x1,y0,x1,y1,width=width,dash=(width,width))
        canvas.create_line(x1,y1,x0,y1,width=width,dash=(width,width))
        canvas.create_line(x0,y1,x0,y0,width=width,dash=(width,width))


###############################
# Misc. Functions
###############################

def changeSplashScreen(mode,data): # changes data.mode to parameter mode
    data.mode = mode
    # runs presets for modes
    if mode == "workspace":
        data.matrices = []
        data.numbers = []
        data.selectedCell = []
    elif mode == "lesson1":
        lesson1Presets(data)
    elif mode == "lesson2":
        lesson2Presets(data)
    elif mode == "lesson3":
        lesson3Presets(data)
    elif mode == "lesson4":
        lesson4Presets(data)
    elif mode == "lesson5":
        lesson5Presets(data)
    elif mode == "lesson6":
        lesson6Presets(data)
    elif mode == "lesson7":
        lesson7Presets(data)
    elif mode == "lesson8":
        lesson8Presets(data)

def drawBrackets(self,canvas,margin,numberSepX,numberSepY,numberWidth):
        # draws brackets, where x0,y0 is top left corner of matrix
        rows = len(self.values)
        cols = len(self.values[0])
        x0,y0 = self.x, self.y
        cornerLength = 10 # length of ribbet on bracket
        extra = 5 # extra padding between bottom row and bracket
        x1 = x0 + margin*2 + numberWidth*cols + numberSepX*(cols-1)
        y1 = y0 + margin*2 + numberSepY*rows + numberSepY*(rows-1) + extra
        lineWidth = 5
        canvas.create_rectangle(x0,y0,x1,y1,fill="white",
                                outline="black",width=lineWidth)
        canvas.create_line(x0+cornerLength,y0,x1-cornerLength,y0,fill="white",
                            width=lineWidth)
        canvas.create_line(x0+cornerLength,y1,x1-cornerLength,y1,fill="white",
                            width=lineWidth)

def isLegalAdd(matrix1, matrix2):
    #checks if two matrices can be added (dimensions must be the same)
    #it suffices to check first row because all matrices are non-ragged 2d list
    return len(matrix1.values) == len(matrix2.values) and \
    len(matrix1.values[0]) == len(matrix2.values[0])

def addMatrix(data,matrix1,matrix2):
    #resets colors to black
    matrix1.color = "black"
    matrix2.color = "black"
    # adds two matrix objects, creates resulting matrix
    if isLegalAdd(matrix1,matrix2):
        result = make2dList(len(matrix1.values),len(matrix1.values[0]))
        for i in range(len(result)):
            for j in range(len(result[0])):
                result[i][j] = matrix1.values[i][j]+matrix2.values[i][j]
        x,y = data.width/2, data.height/2 # center of screen
        history = ["+", matrix1,matrix2]
        data.matrices.append(Matrix(result,x,y,history))
    else:
        #colors the matrices red if they can't be added
        matrix1.color = "red"
        matrix2.color = "red"

def subtractMatrix(data,matrix1,matrix2):
    #resets colors to black
    matrix1.color = "black"
    matrix2.color = "black"
    # adds two matrix objects, creates resulting matrix
    if isLegalAdd(matrix1,matrix2):
        result = make2dList(len(matrix1.values),len(matrix1.values[0]))
        for i in range(len(result)):
            for j in range(len(result[0])):
                result[i][j] = matrix1.values[i][j]-matrix2.values[i][j]
        x,y = data.width/2, data.height/2 # center of screen
        history = ["-", matrix1,matrix2]
        data.matrices.append(Matrix(result,x,y,history))
    else:
        #colors the matrices red if they can't be subtracted
        matrix1.color = "red"
        matrix2.color = "red"


def isLegalMultiply(matrix1, matrix2):
    #checks if two matrices can be multiplied (#row matrix1 = #cols matrix2)
    return len(matrix1.values[0]) == len(matrix2.values)

def multiply(data,object1,object2):
    if isinstance(object1,Matrix) and isinstance(object2,Matrix):
        # matrix times matrix (order of matters)
        matrixTimesMatrix(data,object1,object2)
    elif isinstance(object1,Number) and isinstance(object2,Matrix):
        # matrix times number
        matrixTimesNumber(data,object2,object1)
    elif isinstance(object2,Number) and isinstance(object1,Matrix):
        # same as above but order switched
        matrixTimesNumber(data,object1,object2)


def matrixTimesMatrix(data,matrix1,matrix2): #multiplies two matrices
    #resets colors to black
    matrix1.color = "black"
    matrix2.color = "black"
    #multiplies matrix1 by matrix2, creates resulting matrix
    if isLegalMultiply(matrix1,matrix2):
        #x,y for resulting matrix
        x,y = data.width/2, data.height/2
        result = np.matmul(matrix1.values,matrix2.values)
        result = list(result)
        for row in range(len(result)):
            result[row] = list(result[row])
        history = ["x", matrix1,matrix2]
        data.matrices.append(Matrix(result,x,y,history))
    else:
        #colors the matrices red if they can't be multiplied
        matrix1.color = "red"
        matrix2.color = "red"

def matrixTimesNumber(data,matrix,number):
    # copies matrix
    result = copy.deepcopy(matrix.values)
    scalar = number.value
    for row in range(len(result)):
        for col in range(len(result[0])):
            # multiplies each entry by scalar
            result[row][col] *= scalar
    #x,y for resulting matrix
    x,y = data.width/2, data.height/2
    # creates new matrix
    history = ["cx", number,matrix]
    data.matrices.append(Matrix(result,x,y,history))


def findMatrixCell(matrix,x,y):
    # returns (row,col) tuple of cell user has right clicked on
    margin = 10 # space between number and bracket
    numberSepX = 20 # space between numbers side by side
    numberSepY = 15 # space between numbers vertically
    numberWidth = getNumberWidth(matrix.values)  # largest number width
    for row in range(len(matrix.values)):
        for col in range(len(matrix.values[0])):
            x0 = matrix.x + margin + numberSepX*(col) + numberWidth*col
            y0 = matrix.y + margin + numberSepY*(row) + numberSepY*row
            x1 = x0 + numberWidth
            y1 = y0 + numberSepY
            if x > x0 and x < x1 and y > y0 and y<y1: # contains click
                return (row,col)


def make2dList(rows, cols):
    # taken from notes
    # creates a 2d list with size rows x cols
    L=[]
    for row in range(rows): L += [[0]*cols]
    return L

def roundList(L):
    # converts floats to ints if they are whole numbers, otherwise rounds to
    # one decimal place
    for row in range(len(L)):
        for col in range(len(L[0])):
            if int(L[row][col]) == L[row][col]:
                L[row][col] = int(L[row][col])
            else: 
                L[row][col] = round(L[row][col],2)
    return L

def getNumberWidth(L):
    # returns width of the largest digit in a list
    digitWidth = 10 # horizontal width of a number
    longest = 0 # length of longest digit in matrix
    for row in range(len(L)):
        for col in range(len(L[0])):
            if len(str(L[row][col])) > longest:
                longest = len(str(L[row][col]))
    return longest*digitWidth


def drawRoundedRectangle(canvas,data,x,y,width,height,color,borderColor):
    # draws a rectangle with rounded corners
    d = 40 # diameter of corners
    line = 5 # border line width
    # draws circles
    x0,y0,x1,y1 = x,y,x+d,y+d
    canvas.create_oval(x0,y0,x1,y1,fill=color,outline=borderColor,width=line)
    x0,y0,x1,y1 = x+width-d,y,x+width,y+d
    canvas.create_oval(x0,y0,x1,y1,fill=color,outline=borderColor,width=line)
    x0,y0,x1,y1 = x+width-d,y+height-d,x+width,y+height
    canvas.create_oval(x0,y0,x1,y1,fill=color,outline=borderColor,width=line)
    x0,y0,x1,y1 = x,y+height-d,x+d,y+height
    canvas.create_oval(x0,y0,x1,y1,fill=color,outline=borderColor,width=line)
    # draws rectangles
    x0,y0,x1,y1 = x,y+d/2,x+width,y+height-d/2
    canvas.create_rectangle(x0,y0,x1,y1,fill=color,outline="black",width=0)
    x0,y0,x1,y1 = x+d/2,y,x+width-d/2,y+height
    canvas.create_rectangle(x0,y0,x1,y1,fill=color,outline="black",width=0)
    #draws lines
    x0,y0,x1,y1 = x+d/2,y,x+width-d/2,y
    canvas.create_line(x0,y0,x1,y1,fill=borderColor,width=line)
    x0,y0,x1,y1 = x+d/2,y+height,x+width-d/2,y+height
    canvas.create_line(x0,y0,x1,y1,fill=borderColor,width=line)
    x0,y0,x1,y1 = x,y+d/2,x,y+height-d/2
    canvas.create_line(x0,y0,x1,y1,fill=borderColor,width=line)
    x0,y0,x1,y1 = x+width,y+d/2,x+width,y+height-d/2
    canvas.create_line(x0,y0,x1,y1,fill=borderColor,width=line)

####################################
# Framework functions
# taken from notes
####################################

def init(data,canvas): # main data structure
    # current mode (mainScreen, helpScreen, workspace, lesson#)
    data.mode = "mainScreen"
    data.time = 0
    data.mouseX = 0
    data.mouseY = 0
    # workspace data
    data.isTyping = False
    data.userInput = ""
    data.showHelp = False
    data.isAdding = False
    data.isSubtracting = False
    data.isMultiplying = False
    data.workspaceHelpScreen = PhotoImage(file="workspaceHelpScreen.gif")
    initExtra(data,canvas)
    initExtraExtra(data,canvas)

def initExtra(data,canvas):
    # lesson data
    data.lesson3Rows = None
    data.lesson3Cols = None
    data.lesson3correct = None
    data.lesson4Operation = None
    data.lesson4Text = ""
    data.lesson5Exercise1Matrices = []
    data.lesson5Exercise2Matrices = []
    data.lesson5correct1 = None
    data.lesson5correct2 = None
    data.lesson6Sizes = None
    data.lesson7Text = ""
    data.lesson8Exercise1Matrices = []
    data.lesson8Exercise2Matrices = []
    data.lesson8Answer1 = None
    data.lesson8correct1 = None
    data.lesson8correct2 = None 
    
def initExtraExtra(data,canvas):
    # objects
    data.matrices = []
    data.numbers = []
    data.selectedObject = None
    data.selectedCell = None
    # list of rainbow colors
    indigoRed, indigoGreen, indigoBlue = 75,0,130
    violetRed, violetGreen, violetBlue = 139,0,255
    data.colors = ["red","orange","yellow","green","blue",
    rgbString(indigoRed,indigoGreen,indigoRed),
    rgbString(violetRed,violetGreen,violetBlue)]
    #numbers
    data.workspaceSideBarWidth = 230
    data.workspaceSeparation = 40

def mouseMotion(event,data):
    # stores location of mouse
    data.mouseX = event.x
    data.mouseY = event.y

def keyPressed(event, data):
    # use event.char and event.keysym
    if data.mode == "workspace":
        workspaceKeyPressed(event,data)
    elif data.mode == "lesson3":
        lesson3KeyPressed(event,data)
    elif data.mode == "lesson5":
        lesson5KeyPressed(event,data)
    elif data.mode == "lesson8":
        lesson8KeyPressed(event,data)

def timerFired(data):
    # timer fired
    data.time += 10
    if data.mode == "lesson1":
        lesson1TimerFired(data)
    elif data.mode == "lesson2":
        lesson2TimerFired(data)
    elif data.mode == "lesson6":
        lesson6TimerFired(data)


def redrawAll(canvas, data):
    # draw in canvas
    if data.mode == "mainScreen": mainScreenRedrawAll(canvas,data)
    elif data.mode == "helpScreen": helpScreenRedrawAll(canvas,data)
    elif data.mode == "workspace":workspaceRedrawAll(canvas,data)
    elif data.mode == "lesson1": lesson1RedrawAll(canvas,data)
    elif data.mode == "lesson2": lesson2RedrawAll(canvas,data)
    elif data.mode == "lesson3": lesson3RedrawAll(canvas,data)
    elif data.mode == "lesson4": lesson4RedrawAll(canvas,data)
    elif data.mode == "lesson5": lesson5RedrawAll(canvas,data)
    elif data.mode == "lesson6": lesson6RedrawAll(canvas,data)
    elif data.mode == "lesson7": lesson7RedrawAll(canvas,data)
    elif data.mode == "lesson8": lesson8RedrawAll(canvas,data)
    elif data.mode == "lesson9": lesson9RedrawAll(canvas,data)

def leftMousePressed(event,canvas,data):
    #calls function in respective mode 
    if data.mode == "workspace":
        workspaceLeftMousePressed(event,canvas,data)
    elif data.mode == "lesson3":
        lesson3LeftMousePressed(event,canvas,data)
    elif data.mode == "lesson5":
        lesson5LeftMousePressed(event,canvas,data)
    elif data.mode == "lesson8":
        lesson8LeftMousePressed(event,canvas,data)


def leftMouseMoved(event,canvas,data): 
    #calls function in respective mode
    if data.mode == "workspace":
        workspaceLeftMouseMoved(event,canvas,data)

def leftMouseReleased(event,canvas,data): 
    #calls function in respective mode
    pass

def rightMousePressed(event,canvas,data):
    # calls function in respective mode
    if data.mode == "workspace":
        workspaceRightMousePressed(event,canvas,data)
    elif data.mode == "lesson4":
        lesson4RightMousePressed(event,canvas,data)
    elif data.mode == "lesson5":
        lesson5RightMousePressed(event,canvas,data)
    elif data.mode == "lesson7":
        lesson7RightMousePressed(event,canvas,data)
    elif data.mode == "lesson8":
        lesson8RightMousePressed(event,canvas,data)


#################################
# mainScreen
#################################

def mainScreenRedrawAll(canvas,data):
    drawTitle(canvas,data)
    mainScreenDrawButtons(canvas,data)
    

def drawTitle(canvas,data): # draws title 'Easy Matricees' with changing color
    mod,six,width = 7, 6, 5
    i = data.time//10%mod
    text = "Easy Matrices"
    canvas.create_rectangle(0,0,data.width,data.height, fill="black")
    x0,y0,x1,y1,cornerLength,textSep = 260,330,740,500,20,50
    byFontSize, gusFontSize, matrixFontSize = 30,40,64
    canvas.create_rectangle(x0,y0,x1,y1,fill="black",outline=data.colors[six-i],
        width=width)
    canvas.create_line(x0+cornerLength,y0,x1-cornerLength,y0,width=width)
    canvas.create_line(x0+cornerLength,y1,x1-cornerLength,y1,width=width)
    canvas.create_text(data.width/2,data.height/2+textSep,text="by",
        fill=data.colors[i],font=("comic sans ms",byFontSize, "bold", "italic"))
    canvas.create_text(data.width/2,data.height/2+textSep*2,
        text="Gustavo Angulo",fill=data.colors[i],
        font=("comic sans ms", gusFontSize, "bold", "italic"))
    canvas.create_text(data.width/2,data.height/2,text=text,fill=data.colors[i],
        font=("comic sans ms", matrixFontSize, "bold", "italic"))

def mainScreenDrawButtons(canvas,data):
    # draws Lessons Button
    x, y, width, height, color,padx = 50, 575, 200, 50, 4, 50
    drawRoundedRectangle(canvas,data,x,y,width,height,data.colors[color],
        data.colors[color])
    lessonsX,lessonsY = 147,600
    lessons = Button(canvas,padx=padx,text="Lessons",
        highlightbackground=data.colors[color],
        command=lambda : changeSplashScreen("lesson1",data))
    canvas.create_window(lessonsX,lessonsY,window=lessons)
    # draws Workspace button
    x, y, width, height, color = 420, 575, 200, 50, 5
    drawRoundedRectangle(canvas,data,x,y,width,height,data.colors[color],
        data.colors[color])
    workspaceX,workspaceY = 520,600
    workspace = Button(canvas,padx=padx,text="Workspace",
        highlightbackground=data.colors[color],
        command=lambda : changeSplashScreen("workspace",data))
    canvas.create_window(workspaceX,workspaceY,window=workspace)
    # draws help button
    x, y, width, height, color = 755, 575, 200, 50, 6
    drawRoundedRectangle(canvas,data,x,y,width,height,data.colors[color],
        data.colors[color])
    helpX,helpY = 858,600
    helpScreen = Button(canvas,padx=padx,text="About",bg="red",
        highlightbackground=data.colors[color],
        command=lambda : changeSplashScreen("helpScreen",data))
    canvas.create_window(helpX,helpY,window=helpScreen)


#################################
# help screen
#################################



def helpScreenRedrawAll(canvas,data):
    # draw background
    canvas.create_rectangle(0,0,data.width,data.height,fill="black")
    # draw buttons
    helpscreenDrawButtons(canvas,data)
    # draw text
    helpScreenDrawText(canvas,data)


def helpscreenDrawButtons(canvas,data):
    # draws Lessons Button
    lessonsX,lessonsY,padx = 225,275, 55
    lessons = Button(canvas,padx=padx,text="Lessons",highlightbackground="blue",
        command=lambda : changeSplashScreen("lesson1",data))
    canvas.create_window(lessonsX,lessonsY,window=lessons)
    # draws Workspace button
    workspaceX,workspaceY,padx,color = 225,350,50, 5
    workspace = Button(canvas,padx=padx,text="Workspace",
        highlightbackground=data.colors[color],
        command=lambda : changeSplashScreen("workspace",data))
    canvas.create_window(workspaceX,workspaceY,window=workspace)
    # draws mainscreen button
    helpX,helpY,color,padx = 225,425, 6, 45
    mainScreen = Button(canvas,padx=padx,text="Main Screen",
        highlightbackground=data.colors[color],
        command=lambda : changeSplashScreen("mainScreen",data))
    canvas.create_window(helpX,helpY,window=mainScreen)
    drawButtonInfo(canvas,data)


def drawButtonInfo(canvas,data):
    blueIndex,factor,recStartY,explaStartY,separation = 4, 8, 250,275, 75
    startY = 250
    colors = data.colors[4:]
    text = [': Learn the fundementals of matrix algebra!',
            ': Create and work with matrices visually!',
            ': Go back to the main screen']
    for i in range(len(colors)):
        x, y, width, height = data.width/factor, startY + separation*i, 200, 50
        drawRoundedRectangle(canvas,data,x,y,width,height,colors[i],colors[i])
        x,y,fontSize = 330,explaStartY + separation*i, 30
        canvas.create_text(x,y,anchor=W, text=text[i], fill=colors[i],
        font=("comic sans ms", fontSize))
    

def helpScreenDrawText(canvas,data):
    # draw "About"
    x,y,aboutFontSize = data.width/2, 50,50
    canvas.create_text(x,y,text="About", fill="Red",
        font=("comic sans ms", aboutFontSize, "bold", "underline"))
    # draw who
    factor = 8
    x,y,aboutFontSize = data.width/factor, 100,30
    text = "Who: Gustavo Angulo"
    canvas.create_text(x,y,text=text, fill="Orange", anchor=NW,
        font=("comic sans ms", aboutFontSize))
    # draw what
    x,y,aboutFontSize = data.width/factor, 150,30
    text = "What: Interactive matrix teaching module"
    canvas.create_text(x,y,text=text, fill="Yellow", anchor=NW,
        font=("comic sans ms", aboutFontSize))
    # draw why
    x,y,aboutFontSize = data.width/factor, 200,30
    text = "Why: 15-112 Fall 2015 Term Project"
    canvas.create_text(x,y,text=text, fill="Green", anchor=NW,
        font=("comic sans ms", aboutFontSize))

#################################
# workspace
#################################

def workspaceKeyPressed(event,data):
    if event.keysym == "Escape": # breaks out of typing or operations
        data.isTyping = False
        data.isAdding = False
        data.isSubtracting = False
        data.isMultiplying = False
        data.selectedObject = None
        data.userInput = ""
        for matrix in data.matrices: # unhighlights cells
            matrix.highlightedValues = []
    if data.isTyping == False: # keyboard shortcuts
        workspaceKeyboardShortcuts(event,data)
    elif event.keysym == "Return": # user finishes typing
        workspaceUserTyping(event,data)
    else: # user adds a number
        if event.keysym.isdigit(): data.userInput += event.keysym
        elif event.keysym == "minus": #adds a negative sign
            data.userInput = "-" + data.userInput


def workspaceKeyboardShortcuts(event,data):
    shiftComparison = 0x0001
    shift = ((event.state & shiftComparison) != 0)
    if event.keysym == "h": toggleWorkspaceHelp(data)
    elif event.keysym == "m": makeMatrix(data,data.mouseX,data.mouseY)
    elif event.keysym == "n": makeNumber(data,data.mouseX,data.mouseY)
    elif event.keysym == "d": deleteObject(data)
    elif event.keysym == "c": clearWorkSpace(data)
    elif event.keysym == "plus" and shift == True: isAdding(data)
    elif event.keysym == "minus": isSubtracting(data)
    elif event.keysym == "x": isMultiplying(data)
    elif data.selectedObject != None and \
    isinstance(data.selectedObject,Matrix): # changes size of select matrix
        if event.keysym == "Up": data.selectedObject.deleteRow()
        elif event.keysym == "Down": data.selectedObject.addRow()
        elif event.keysym == "Left": data.selectedObject.deleteCol()
        elif event.keysym == "Right": data.selectedObject.addCol()

def workspaceUserTyping(event,data):       
    if isinstance(data.selectedObject,Number): # changes number
        try: data.selectedObject.value = int(data.userInput)
        except: pass
        data.userInput = ""
        data.isTyping = False
        data.selectedObject = None
    elif isinstance(data.selectedObject,Matrix): # changes matrix cell
        row,col = data.selectedCell
        try: data.selectedObject.values[row][col] = int(data.userInput)
        except: pass # ignores input if causes error
        data.selectedObject.highlightedValues = []
        data.userInput = ""
        data.isTyping = False
        data.selectedObject.history = None
        data.selectedObject = None
        

def workspaceRedrawAll(canvas,data):
    drawWorkspaceUI(canvas,data)
    workspaceDrawButtons(canvas,data)
    # draws matrices
    for matrix in data.matrices: matrix.draw(canvas)
    # draws numbers
    for number in data.numbers: number.draw(canvas)
    # draws dashed selection
    if data.selectedObject != None:
        data.selectedObject.drawDash(canvas)
        if data.selectedObject.history != None: 
            drawHistory(canvas,data)
    # draws current operation
    x,y = data.width-50, 80
    if data.isTyping == True and data.userInput != "": # user changing number
        canvas.create_text(x,y,text=str(data.userInput), fill="blue", anchor=SE,
            font="Times 60")
    elif data.isAdding == True:
        canvas.create_text(x,y,text="+", fill="blue", anchor=SE,font="Times 60")
    elif data.isSubtracting == True:
        canvas.create_text(x,y,text="-", fill="blue", anchor=SE,font="Times 60")
    elif data.isMultiplying == True:
        canvas.create_text(x,y,text="x", fill="blue", anchor=SE,font="Times 60")
    # draws help
    if data.showHelp == True:
        drawHelp(canvas,data)

def workspaceLeftMousePressed(event,canvas,data):
    clickedOnObject = False
    if data.isTyping == False: # locks user from clicking if typing
        # selects matrix if clicked on
        if workspaceLeftMousePressedMatrix(event,canvas,data):
            clickedOnObject = True
        elif workspaceLeftMousePressedNumber(event,canvas,data):
            clickedOnObject = True
        # unselects object if clicked on empty space
        if clickedOnObject == False and event.x > data.workspaceSideBarWidth:
            data.selectedObject = None


def workspaceLeftMousePressedMatrix(event,canvas,data):
    # returns True if user clicks on a matrix
    for matrix in data.matrices:
        if matrix.matrixContainsClick(event.x,event.y):
            if data.isAdding: # add matrices
                if isinstance(data.selectedObject,Matrix) and \
                isinstance(matrix,Matrix):
                    addMatrix(data,data.selectedObject,matrix)
                    data.isAdding = False
                # user does not select two matrices
                else: data.selectedObject,data.isAdding = None, False
            elif data.isSubtracting:
                if isinstance(data.selectedObject,Matrix) and \
                isinstance(matrix,Matrix):
                    # subtracts matrces
                    subtractMatrix(data,data.selectedObject,matrix)
                    data.isSubtracting = False
                # user does not select two matrices
                else: data.selectedObject,data.isSubtracting = None, False
            elif data.isMultiplying: # multiplies
                multiply(data,data.selectedObject,matrix)
                data.isMultiplying,data.selectedObject = False, None
            else: data.selectedObject = matrix # selecting matrix
            return True

def workspaceLeftMousePressedNumber(event,canvas,data):
    # returns true if number is clicked on
    # selects number if clicked on
    for number in data.numbers:
        if number.numberContainsClick(event.x,event.y):
            if data.isMultiplying:
                multiply(data,data.selectedObject,number)
                data.isMultiplying = False
            else:
                data.selectedObject = number
            return True
        


def workspaceLeftMouseMoved(event,canvas,data):
    if data.isTyping == False: # locks user out if typing
        # moves around selected object
        if data.selectedObject != None:
            data.selectedObject.x = event.x
            data.selectedObject.y = event.y


def workspaceRightMousePressed(event,canvas,data):
    # locks user out if typing
    if data.isTyping == False:
        clickedOnObject = False
        # selects number if clicked on 
        for number in data.numbers:
            if number.numberContainsClick(event.x,event.y):
                data.selectedObject = number
                clickedOnObject = True # user clicked on object
                data.isTyping = True # user is going to type
        # selects matrix if clicked on
        for matrix in data.matrices:
            if matrix.matrixContainsClick(event.x,event.y):
                if findMatrixCell(matrix,event.x,event.y) != None:
                    data.selectedObject = matrix
                    (row,col) = findMatrixCell(matrix,event.x,event.y)
                    data.selectedCell = (row,col)
                    matrix.highlightedValues.append((row,col)) # highlight cell
                    clickedOnObject = True # user clicked on object
                    data.isTyping = True # user is going to type
        if clickedOnObject == False and event.x > data.workspaceSideBarWidth:
            # unselects object if clicked on empty space
            data.selectedObject = None

def drawWorkspaceUI(canvas,data):
    # draw black background
    canvas.create_rectangle(0,0,data.width,data.height,fill="black")
    # green button backgrounds
    x,y,width,height = data.workspaceSeparation,data.workspaceSeparation,140,460
    drawRoundedRectangle(canvas,data,x,y,width,height,"green","green")
    # white workspace
    x,y,width,height = 230,data.workspaceSeparation,700,650
    drawRoundedRectangle(canvas,data,x,y,width,height,"white","green")
    # draws "Workspace" in button rectangle
    x,y,text = 50,50, "Workspace"
    canvas.create_text(x,y,text=text, fill="black", anchor=NW,
            font=("comic sans ms", 20, "bold"))
    # draw typing rectangle
    x,y,width,height = 830,10,130,70
    drawRoundedRectangle(canvas,data,x,y,width,height,"white","blue")

def drawHistory(canvas,data):
    # draw history rectangle
    verticalShift = 225
    x,y,width,height = 25, data.height - verticalShift, 400,200
    drawRoundedRectangle(canvas,data,x,y,width,height,"white","red")
    # draws history depending on how matrix was made
    if data.selectedObject.history[0] == "+":
        drawAddHistory(canvas,data)
    elif data.selectedObject.history[0] == "-":
        drawSubtractHistory(canvas,data)
    elif data.selectedObject.history[0] == "x":
        drawMultiplyHistory(canvas,data)
    elif data.selectedObject.history[0] == "T":
        drawTransposeHistory(canvas,data)
    elif data.selectedObject.history[0] == "-1":
        drawInverseHistory(canvas,data)
    elif data.selectedObject.history[0] == "2":
        drawSquareHistory(canvas,data)
    elif data.selectedObject.history[0] == "det":
        drawDeterminantHistory(canvas,data)
    elif data.selectedObject.history[0] == "cx":
        drawScalarMultiplyHistory(canvas,data)

def drawAddHistory(canvas,data):
    # draws matrices and operation that created resulting matrix 
    # draw first matrix 
    values = data.selectedObject.history[1].values
    centerX, centerY = 125,635
    x,y = topLeftOfMatrix(values, centerX, centerY)
    Matrix(values,x,y).draw(canvas)
    # draw "+"
    fontSize = 60
    x,y,font = 220, centerY,("comic sans ms",fontSize)
    canvas.create_text(x,y,text="+",font=font,fill="red")
    # draw second matrix
    values = data.selectedObject.history[2].values
    centerX, centerY = 325, 635
    x,y = topLeftOfMatrix(values, centerX, centerY)
    Matrix(values,x,y).draw(canvas)


def drawSubtractHistory(canvas,data):
    # draws matrices and operation that created resulting matrix 
    # draw first matrix
    values = data.selectedObject.history[1].values
    centerX,centerY = 125, 635
    x,y = topLeftOfMatrix(values, centerX,centerY)
    Matrix(values,x,y).draw(canvas)
    # draw "-"
    fontSize = 60
    x,y,font = 220, 625,("comic sans ms",fontSize)
    canvas.create_text(x,y,text="-",font=font,fill="red")
    # draw second matrix
    values = data.selectedObject.history[2].values
    centerX,centerY = 335, 635
    x,y = topLeftOfMatrix(values, centerX, centerY)
    Matrix(values,x,y).draw(canvas)

def drawMultiplyHistory(canvas,data):
    # draws matrices and operation that created resulting matrix 
    # draw first matrix
    values = data.selectedObject.history[1].values
    centerX,centerY = 125, 635
    x,y = topLeftOfMatrix(values,centerX,centerY)
    Matrix(values,x,y).draw(canvas)
    # draw "x"
    fontSize = 60
    x,y,font = 220,625,("comic sans ms",fontSize)
    canvas.create_text(x,y,text="x",font=font,fill="red")
    # draw second matrix
    values = data.selectedObject.history[2].values
    centerX,centerY = 335, 635
    x,y = topLeftOfMatrix(values, centerX,centerY)
    Matrix(values,x,y).draw(canvas)

def drawTransposeHistory(canvas,data):
    # draw Matrix
    values = data.selectedObject.history[1].values
    centerX,centerY = 220, 635
    x,y = topLeftOfMatrix(values,centerX,centerY)
    Matrix(values,x,y).draw(canvas)
    # draw transpose "T"
    x,y = topRightOfMatrix(values,x,y)
    fontSize = 30
    font = ("Helvetica",fontSize)
    canvas.create_text(x,y,text="T",anchor=W,fill="black",font=font)


def topRightOfMatrix(values,x,y):
    # given x,y for top left of matrix, returns x,y for top right of matrix
    cols = len(values[0])
    numberWidth = getNumberWidth(values)
    numberSepX = 20
    margin = 10
    x = x + margin*2 + numberWidth*cols + numberSepX*(cols-1)
    return (x,y) # y doesnt change

def drawInverseHistory(canvas,data):
    # draw Matrix
    values = data.selectedObject.history[1].values
    centerX,centerY = 220, 635
    x,y = topLeftOfMatrix(values,centerX,centerY)
    Matrix(values,x,y).draw(canvas)
    # draw inverse "-1"
    x,y = topRightOfMatrix(values,x,y)
    x = x + 10 # add shift to -1
    fontSize = 30
    font = ("Helvetica",fontSize)
    canvas.create_text(x,y,text="-1",anchor=W,fill="black",font=font)

def drawSquareHistory(canvas,data):
    # draw Matrix
    values = data.selectedObject.history[1].values
    centerX,centerY = 220, 635
    x,y = topLeftOfMatrix(values,centerX,centerY)
    Matrix(values,x,y).draw(canvas)
    # draw square "^2"
    x,y = topRightOfMatrix(values,x,y)
    x = x + 10 # add shift to ^2
    fontSize = 30
    font = ("Helvetica",fontSize)
    canvas.create_text(x,y,text="2",anchor=W,fill="black",font=font)

def drawDeterminantHistory(canvas,data):
    # draw Matrix
    values = data.selectedObject.history[1].values
    centerX,centerY = 220, 635
    x,y = topLeftOfMatrix(values,centerX,centerY)
    Matrix(values,x,y).draw(canvas)
    width = (centerX-x)*2
    # draw left "det("
    x,y = x - 10, 635
    fontSize = 60
    font = ("Helvetica",fontSize)
    canvas.create_text(x,y,anchor=E,text="det(",font=font)
    # draw right ")"
    shiftRight = 20 
    x = x + width + shiftRight
    canvas.create_text(x,y,anchor=W,text=")",font=font)

def drawScalarMultiplyHistory(canvas,data):
    # draw Matrix
    values = data.selectedObject.history[2].values
    centerX,centerY = 220, 635
    x,y = topLeftOfMatrix(values,centerX,centerY)
    Matrix(values,x,y).draw(canvas)
    # draw number
    value = data.selectedObject.history[1].value
    numberLeftShift = 40
    x,y = x - numberLeftShift, 625
    Number(value,x,y).draw(canvas)

def workspaceDrawButtons(canvas,data):
    # draws buttons in side bar
    # list of button labels
    buttons = ["Main Screen","Help (h)", "New Matrix (m)", 
    "New Number (n)", "Delete (d)", "Clear (c)", "Add (+)", "Subtract (-)",
    "Multiply (x)", "Transpose", "Inverse", "M^2", "Determinant", 
    "Solve system"]
    defaultX, defaultY = data.width/2, data.height/2
    # list of commands for buttons
    commands = [(lambda:changeSplashScreen('mainScreen',data)),
                (lambda:toggleWorkspaceHelp(data)), 
                (lambda:makeMatrix(data,defaultX,defaultY)), 
                (lambda:makeNumber(data,defaultX,defaultY)),
                (lambda:deleteObject(data)), 
                (lambda:clearWorkSpace(data)),
                (lambda:isAdding(data)),
                (lambda:isSubtracting(data)),
                (lambda:isMultiplying(data)),
                (lambda:transpose(data)),
                (lambda:inverse(data)),
                (lambda:squareMatrix(data)),
                (lambda:determinant(data)),
                (lambda:solveMatrixSystem(data))]
    workspaceCreateButtons(canvas,data,buttons,commands)


def workspaceCreateButtons(canvas,data,buttons,commands):
    # creates buttons on workspace given list of commands and buttons
    topSep = 30
    margin = 10 # space between buttons
    size = 20 # size of buttons
    for i in range(len(buttons)):
        # x,y is top left of button
        x = margin + data.workspaceSeparation
        y = topSep + margin + data.workspaceSeparation + margin*i + size*i
        button = Button(canvas, text=buttons[i],highlightbackground="green",
         command=commands[i])
        canvas.create_window(x, y, anchor=NW, window=button)

def drawHelp(canvas,data):
    # draws help pop up
    x,y,width,height = 230,data.workspaceSeparation,550,650
    drawRoundedRectangle(canvas,data,x,y,width,height,"white","red")
    rightShift = 5
    x,y = 250, data.workspaceSeparation + rightShift
    canvas.create_image(x,y,anchor=NW,image=data.workspaceHelpScreen)

def toggleWorkspaceHelp(data):
    # toggles wether helps screen is showing
    data.showHelp = not data.showHelp

def makeMatrix(data,x,y):
    # creates a new matrix in the center of the workspace, or if key shortcut
    # is pressed, at mouse location
    baseMatrix = [[1,1],[1,1]]
    data.matrices.append(Matrix(baseMatrix,x,y))

def makeNumber(data,x,y):
    # creates a new number in the center of the workspace, or if key shortcut
    # is pressed, at mouse location
    data.numbers.append(Number(1,x,y))

def deleteObject(data):
    # deletes currently selected object
    if isinstance(data.selectedObject,Matrix): # if object is a matrix
        data.matrices.remove(data.selectedObject)
        data.selectedObject = None
    elif isinstance(data.selectedObject,Number): # if object is a number
        data.numbers.remove(data.selectedObject)
        data.selectedObject = None

def clearWorkSpace(data):
    # deletes all matrices and objects on workspace
    data.matrices = []
    data.numbers = []
    data.selectedObject = None

def isAdding(data):
    if data.selectedObject != None: # makes sure user has selected an object
        # toggles settings
        data.isAdding,data.isSubtracting,data.isMultiplying = True, False, False

def isSubtracting(data):
    if data.selectedObject != None: # makes sure user has selected an object
        # toggles settings
        data.isAdding,data.isSubtracting,data.isMultiplying = False, True, False

def isMultiplying(data):
    if data.selectedObject != None: # makes sure user has selected an object
        # toggles settings
        data.isAdding,data.isSubtracting,data.isMultiplying = False, False, True

def transpose(data):
    # makes sure user has selected an object
    if data.selectedObject != None and isinstance(data.selectedObject,Matrix):
        # runs transpose method on selected object
        data.selectedObject.transpose(data)

def inverse(data):
    # makes sure user has selected an object
    if data.selectedObject != None and isinstance(data.selectedObject,Matrix):
        # runs inverse method on selected object
        data.selectedObject.findInverse(data)

def squareMatrix(data):
    # makes sure user has selected an object
    if data.selectedObject != None and isinstance(data.selectedObject,Matrix):
        # runs square method on selected object
        data.selectedObject.square(data)

def determinant(data):
    # makes sure user has selected an object
    if data.selectedObject != None and isinstance(data.selectedObject,Matrix):
        # runs determinant method on selected object
        data.selectedObject.findDeterminant(data)

def solveMatrixSystem(data):
    # makes sure user has selected an object
    if data.selectedObject != None and isinstance(data.selectedObject,Matrix):
        # runs solve system method on selected object
        data.selectedObject.solveSystem(data)





#################################
# Lesson 1: What is a Matrix?
#################################


def lesson1TimerFired(data):
    lesson1Presets(data)

def lesson1RedrawAll(canvas,data):
    # draw black background
    canvas.create_rectangle(0,0,data.width,data.height,fill="black")
    drawLessonButtons(canvas,data,"mainScreen","lesson2")
    drawLessonTitle(canvas,data,"What is a Matrix?")
    # draw definition of matrix
    fontSize = 30
    x,y,font = data.width/2, 200, ("comic sans ms",fontSize)
    text = "A matrix is a rectangular grid of numbers"
    canvas.create_text(x,y,text=text,fill="white",font=font)
    # draw definition entries
    fontSize = 30
    x,y,font = data.width/2, 600, ("comic sans ms",fontSize)
    text = "Each number is an entry in the matrix"
    canvas.create_text(x,y,text=text,fill="white",font=font)
    # draws example matrix
    width, height = 400, 300
    x, y = data.width/2 - width/2, 250
    drawRoundedRectangle(canvas,data,x,y,width,height,"white","green")
    for matrix in data.matrices:
        matrix.draw(canvas)  

def lesson1Presets(data): # sets presets for lesson, creates example matrix
    data.matrices = []
    data.selectedObject = None
    maxSize = 4
    values=make2dRandomList(random.randint(1,maxSize),random.randint(1,maxSize))
    centerX, centerY = data.width/2, 390
    x,y = topLeftOfMatrix(values,centerX,centerY)
    data.matrices.append(Matrix(values,x,y,None,True))

#################################
# Lesson 2: Rows and Columns
#################################


def lesson2TimerFired(data):
    lesson2Presets(data)

def lesson2RedrawAll(canvas,data):
    # draw black background
    canvas.create_rectangle(0,0,data.width,data.height,fill="black")
    drawLessonButtons(canvas,data,"lesson1","lesson3")
    drawLessonTitle(canvas,data,"Rows and Columns")
    # draw size explanation
    fontSize = 30
    x,y,font = data.width/2, 200, ("comic sans ms",fontSize)
    text = "A matrix's size is written as rows x columns"
    canvas.create_text(x,y,text=text,fill="white",font=font)
    # draws example area
    width, height = 400, 300
    x,y = data.width/2 - width/2, 250
    drawRoundedRectangle(canvas,data,x,y,width,height,"white","green")
    for matrix in data.matrices: matrix.draw(canvas)
    drawArrows(canvas,data)
    # draw example explanation
    fontSize = 30
    x,y,font = data.width/2, 600, ("comic sans ms",fontSize)
    text = "For example, the matrix above is 3x3"
    canvas.create_text(x,y,text=text,fill="white",font=font)



def drawArrows(canvas,data): # draws arrows for example
    drawColumnArrows(canvas,data)
    drawRowArrows(canvas,data)


def drawColumnArrows(canvas,data): # draws arrows indicating columns
    # draws columns
    x,y,fontSize = data.width/2, 275,20
    canvas.create_text(x,y,text="Columns",fill="blue",
        font=("comic sans ms",fontSize,"underline"))
    leftArrowX, rightArrowX = 455, 540
    arrowsX,width = [leftArrowX,data.width/2,rightArrowX], 3
    for i in range(len(arrowsX)):
        x0,y0,x1,y1 = arrowsX[i],290,arrowsX[i],330
        canvas.create_line(x0,y0,x1,y1,fill="blue",width=width,arrow=LAST)
        y0,y1 = 515,450
        canvas.create_line(x0,y0,x1,y1,fill="blue",width=width,arrow=LAST)
        verticalShift = 15
        fontSize = 20
        y0 = y0 + verticalShift
        canvas.create_text(x0,y0,text=str(i+1),fill="blue",
        font=("comic sans ms",fontSize))

def drawRowArrows(canvas,data): # draws arrows indicating rows
    # draws rows
    x,y,numberOfArrows = 340,395, 3
    canvas.create_text(x,y,text="Rows",fill="red",
        font=("comic sans ms",20,"underline"))
    topArrowY,middleArrowY,bottomArrowY = 365,395,425
    arrowsY = [topArrowY,middleArrowY,bottomArrowY]
    for i in range(numberOfArrows):
        x0,y0,x1,y1,width = 375,arrowsY[i],425,arrowsY[i],3
        canvas.create_line(x0,y0,x1,y1,fill="red",width=width,arrow=LAST)
        x0,x1 = 575, 625
        canvas.create_line(x0,y0,x1,y1,fill="red",width=width,arrow=FIRST)
        x0, fontSize = x1 + 10, 20
        canvas.create_text(x0,y0,text=str(i+1),fill="red",
        font=("comic sans ms",fontSize))

def lesson2Presets(data): # sets presets for lesson, creates example matrix
    data.matrices = []
    size = 3
    values = make2dRandomList(size,size)
    centerX,centerY = data.width/2, 405
    x,y = topLeftOfMatrix(values,centerX,centerY)
    data.matrices.append(Matrix(values,x,y,None,True))

#######################################
# Lesson 3: Rows and Columns Exercise
#######################################

def lesson3KeyPressed(event,data):
    if data.selectedObject != None: # changes size of select matrix
        if event.keysym == "Up": data.selectedObject.deleteRow()
        elif event.keysym == "Down": data.selectedObject.addRow()
        elif event.keysym == "Left": data.selectedObject.deleteCol()
        elif event.keysym == "Right": data.selectedObject.addCol()

def lesson3RedrawAll(canvas,data):
    # draw black background
    canvas.create_rectangle(0,0,data.width,data.height,fill="black")
    drawLessonButtons(canvas,data,"lesson2","lesson4")
    drawLessonTitle(canvas,data,"Try this exercise!")
    # draws example area
    width, height = 400, 300
    x,y = data.width/2 - width/2, 250
    drawRoundedRectangle(canvas,data,x,y,width,height,"white","green")
    # draws matrix
    for matrix in data.matrices: matrix.draw(canvas)
    # creates check answer buttons
    lesson3ExerciseCheck(canvas,data)
    # draws dashed selection
    if data.selectedObject != None:
        data.selectedObject.drawDash(canvas)
    # draw exercise explanation
    fontSize = 30
    x,y,font = data.width/2, 200, ("comic sans ms",fontSize)
    text = "Make this matrix %dx%d" % (data.lesson3Rows,data.lesson3Cols)
    canvas.create_text(x,y,text=text,fill="white",font=font)
    # draw example explanation
    x,y,font = data.width/2, 600, ("comic sans ms",fontSize)
    text = "Click the matrix, and use the arrow keys to change it's size"
    canvas.create_text(x,y,text=text,fill="white",font=font)


def lesson3LeftMousePressed(event,canvas,data):
    for matrix in data.matrices:
        clickedOnObject = False
        if matrix.matrixContainsClick(event.x,event.y):
            data.selectedObject = matrix
            clickedOnObject = True
        # unselects object if clicked on empty space
        if clickedOnObject == False:
            data.selectedObject = None

def lesson3ExerciseCheck(canvas,data):
    # draw check answer button
    x,y = 900,300
    checkAnswer1 = Button(canvas, text="Check Answer",
        highlightbackground="black",
         command=lambda: lesson3CheckAnswer1(data))
    canvas.create_window(x, y, anchor=NE, window=checkAnswer1)
    # draws correct/incorrect:
    if data.lesson3correct != None:
        if data.lesson3correct == True: text,color = "Correct!","green"
        else: text,color = "Incorrect!", "red"
        fontSize = 30
        x,y,font = 850, 400, ("comic sans ms",fontSize)
        canvas.create_text(x,y,text=text,fill=color,font=font)
    def lesson3CheckAnswer1(data):
        # Changes color to green if correct, red if incorrect
        matrix = data.matrices[0]
        matrix.color = "black"
        if len(matrix.values) == data.lesson3Rows and \
            len(matrix.values[0]) == data.lesson3Cols:
            matrix.color, data.lesson3correct = "green", True
        else:
            matrix.color, data.lesson3correct = "red", False
    # draw new exercise button
    lesson3NewExercise(canvas,data)

def lesson3NewExercise(canvas,data):
    x,y = 900,450
    newExercise = Button(canvas, text="New problem",
        highlightbackground="black",
         command=lambda: newProblem(data))
    canvas.create_window(x, y, anchor=NE, window=newExercise)
    def newProblem(data):
        # creates new matrix
        data.lesson3correct = None
        lesson3Presets(data)

def lesson3Presets(data): # sets presets for lesson, creates exercise matrix
    # creates matrix
    data.matrices = []
    x,y = 400,300
    data.matrices.append(Matrix([[1]],x,y,None,False))
    # sets sizes
    minSize,maxSize = 2,5
    data.lesson3Rows = random.randint(minSize,maxSize)
    data.lesson3Cols = random.randint(minSize,maxSize)

########################################
# Lesson 4: Add and subtract Matrices
########################################

def lesson4KeyPressed(event,data):
    pass

def lesson4TimerFired(data):
    pass

def lesson4RedrawAll(canvas,data):
    # draw black background
    canvas.create_rectangle(0,0,data.width,data.height,fill="black")
    drawLessonButtons(canvas,data,"lesson3","lesson5")
    drawLessonTitle(canvas,data,"Add and Subtract Matrices")
    # draw add/sub explanation
    fontSize = 30
    x,y,font = data.width/2, 200, ("comic sans ms",fontSize)
    text = """To +/- a matrix with another, +/- the corresponding entries"""
    canvas.create_text(x,y,text=text,fill="white",font=font)
    # draw example explanation
    x,y,font = data.width/2, 300, ("comic sans ms",fontSize,"underline")
    text = "Right click the entries below to see how this works!"
    canvas.create_text(x,y,text=text,fill="white",font=font)
    # draw matrix size explanation
    x,y,font = data.width/2, 650, ("comic sans ms",fontSize,"bold")
    text = "The matrices must be the same size!"
    canvas.create_text(x,y,text=text,fill="yellow",font=font)
    # draw exercise
    drawLesson4Exercise(canvas,data)
    lesson4NewExercise(canvas,data)
    # draw equation
    if data.lesson4Text != "":
        x,y,font = data.width/2, 550, ("comic sans ms",fontSize,"bold")
        canvas.create_text(x,y,text=data.lesson4Text,fill="blue",font=font)

def lesson4LeftMousePressed(event,canvas,data):
    pass

def lesson4LeftMouseMoved(event,canvas,data):
    pass

def lesson4LeftMouseReleased(event,canvas,data):
    pass

def lesson4RightMousePressed(event,canvas,data):
    for matrix in data.matrices:
        if matrix.matrixContainsClick(event.x,event.y):
            if findMatrixCell(matrix,event.x,event.y) != None:
                (row,col) = findMatrixCell(matrix,event.x,event.y)
                data.selectedCell = (row,col)
    for matrix in data.matrices:
        matrix.highlightedValues = []
        matrix.highlightedValues.append(data.selectedCell)
    if data.selectedCell != None:
        row, col = data.selectedCell
        data.lesson4Text = "%d %s %d = %d" % (data.matrices[0].values[row][col],
            data.lesson4Operation, data.matrices[1].values[row][col],
            data.matrices[2].values[row][col])

def drawLesson4Exercise(canvas,data):
    #draw rounded rectangle
    width, height = 700, 250
    x,y = data.width/2 - width/2, 350
    drawRoundedRectangle(canvas,data,x,y,width,height,"white","green")
    # draw matrices
    for matrix in data.matrices: matrix.draw(canvas)
    # draw operation and equal sign
    fontSize = 60
    x,y,font = 400, 450, ("comic sans ms",fontSize,"bold")
    canvas.create_text(x,y,text=data.lesson4Operation,fill="blue",font=font)
    x,y,font = 600, 450, ("comic sans ms",fontSize,"bold")
    canvas.create_text(x,y,text="=",fill="blue",font=font)

def lesson4NewExercise(canvas,data): # creates a new exercise
    x,y = 975,435
    newExercise = Button(canvas, text="New problem",
        highlightbackground="black",
         command=lambda: newProblem(data))
    canvas.create_window(x, y, anchor=NE, window=newExercise)
    def newProblem(data):
        # creates new matrices
        lesson4Presets(data)

def lesson4Presets(data): # sets presets for lesson, creates exercise matrices
    data.matrices = []
    data.lesson4Text = ""
    # chooses addition or subtraction
    x = random.randint(0,1)
    if x == 0: data.lesson4Operation = "+"
    else: data.lesson4Operation = "-"
    minSize, maxSize = 2,3
    rows, cols = random.randint(minSize,maxSize),random.randint(minSize,maxSize)
    # creates first matrix
    values1,centerX,centerY = make2dRandomList(rows,cols),300,450
    x,y = topLeftOfMatrix(values1,centerX,centerY)
    data.matrices.append(Matrix(values1,x,y,None,True))
    # creates second matrix
    values2,centerX,centerY = make2dRandomList(rows,cols),500,450
    x,y = topLeftOfMatrix(values2,centerX,centerY)
    data.matrices.append(Matrix(values2,x,y,None,True))
    # creates resulting matrix
    if data.lesson4Operation=="+": values3 = addMatrices(values1,values2)
    else: values3 = subtractMatrices(values1,values2)
    centerX,centerY = 700, 450
    x,y = topLeftOfMatrix(values3,centerX,centerY)
    data.matrices.append(Matrix(values3,x,y,None,True))

#####################################
# Lesson 5: Add/Subtract Exercise
#####################################

def lesson5KeyPressed(event,data):
    if data.selectedObject != None and data.isTyping == False: 
        # changes size of select matrix
        if event.keysym == "Up": data.selectedObject.deleteRow()
        elif event.keysym == "Down": data.selectedObject.addRow()
        elif event.keysym == "Left": data.selectedObject.deleteCol()
        elif event.keysym == "Right": data.selectedObject.addCol()
    else:
        lesson5UserTyping(event,data) # user is typing input

def lesson5UserTyping(event,data): 
    if data.isTyping == True:
        if event.keysym == "Return": # user finishes typing
            # changes matrix cell
            row,col = data.selectedCell
            if data.userInput != "":
                try:
                    data.selectedObject.values[row][col]=int(data.userInput)
                except: # ignores input if causes error
                    pass
            data.selectedObject.highlightedValues = []
            data.userInput = ""
            data.isTyping = False
            data.selectedObject = None
        else: # user adds a number
            if event.keysym.isdigit():
                data.userInput += event.keysym
            elif event.keysym == "minus": # adds a negative sign
                data.userInput = "-" + data.userInput

def lesson5TimerFired(data):
    pass

def lesson5RedrawAll(canvas,data):
    # draw black background
    canvas.create_rectangle(0,0,data.width,data.height,fill="black")
    drawLessonButtons(canvas,data,"lesson4","lesson6")
    drawLessonTitle(canvas,data,"Try this exercise!")
    # draw exercise explanation
    fontSize = 30
    x,y,font = data.width/2, 150, ("comic sans ms",fontSize)
    text = "Right click an entry, type, and press enter to change its value"
    canvas.create_text(x,y,text=text,fill="white",font=font)
    # draws example area
    width, height = 600, 350
    x,y = data.width/2 - width/2, 200
    drawRoundedRectangle(canvas,data,x,y,width,height,"white","green")
    # draws excercises
    drawLesson5Exercise1(canvas,data)
    drawLesson5Exercise2(canvas,data)
    # draws new exercise button
    lesson5NewExercise(canvas,data)
    # draws check answer buttons
    lesson5Exercise1Check(canvas,data)
    lesson5Exercise2Check(canvas,data)
    # draws dashed selection
    if data.selectedObject != None:
        data.selectedObject.drawDash(canvas)
    # draws current operation
    lesson5DrawInput(canvas,data)
    


def lesson5LeftMousePressed(event,canvas,data): # user uses left click
    clickedOnObject = False
    if data.isTyping == False:
        for matrix in data.lesson5Exercise1Matrices:
            if matrix.matrixContainsClick(event.x,event.y) and \
                matrix.locked == False: 
                # selects matrix
                data.selectedObject = matrix
                clickedOnObject = True
        for matrix in data.lesson5Exercise2Matrices:
            if matrix.matrixContainsClick(event.x,event.y) and \
                matrix.locked == False:
                # selects matrix
                data.selectedObject = matrix
                clickedOnObject = True
        # unselects object if clicked on empty space
        if clickedOnObject == False and event.x > data.workspaceSideBarWidth:
            data.selectedObject = None

def lesson5LeftMouseMoved(event,canvas,data):
    pass

def lesson5LeftMouseReleased(event,canvas,data):
    pass

def lesson5RightMousePressed(event,canvas,data):
    if data.isTyping == False:
        clickedOnObject = False
        # selects matrix if clicked on
        if lesson5RightMousePressedMatrix(event,canvas,data):
            clickedOnObject = True
        # unselects object if clicked on empty space
        if clickedOnObject == False and event.x > data.workspaceSideBarWidth:
            data.selectedObject = None
        
def lesson5RightMousePressedMatrix(event,canvas,data):
    # returns true if a cell in a matrix was clicked
    for matrix in data.lesson5Exercise1Matrices:
        if matrix.matrixContainsClick(event.x,event.y) and \
        matrix.locked == False:
            if findMatrixCell(matrix,event.x,event.y) != None:
                data.selectedObject = matrix
                (row,col) = findMatrixCell(matrix,event.x,event.y)
                data.selectedCell = (row,col)
                matrix.highlightedValues.append((row,col)) # highlight cell
                clickedOnObject,data.isTyping = True, True
                return True
    for matrix in data.lesson5Exercise2Matrices:
        if matrix.matrixContainsClick(event.x,event.y) and \
            matrix.locked == False:
            if findMatrixCell(matrix,event.x,event.y) != None:
                data.selectedObject = matrix
                (row,col) = findMatrixCell(matrix,event.x,event.y)
                data.selectedCell = (row,col)
                matrix.highlightedValues.append((row,col)) # highlight cell
                clickedOnObject,data.isTyping = True, True
                return True
        

def lesson5Exercise1(data): # addition exercse
    # sets random size
    minSize, maxSize = 2,3
    rows, cols = random.randint(minSize,maxSize),random.randint(minSize,maxSize)
    # creates first matrix
    values1 = make2dRandomList(rows,cols)
    centerX,centerY = 300, 300
    x,y = topLeftOfMatrix(values1,centerX,centerY)
    data.lesson5Exercise1Matrices.append(Matrix(values1,x,y,None,True))
    # creates second matrix
    values2 = make2dRandomList(rows,cols)
    centerX,centerY = data.width/2, 300
    x,y = topLeftOfMatrix(values2,centerX,centerY)
    data.lesson5Exercise1Matrices.append(Matrix(values2,x,y,None,True))
    # creates modifiable matrix
    horizontalShift = 190
    x,y = x + horizontalShift, y
    data.lesson5Exercise1Matrices.append(Matrix([[1]],x,y,None,False))

def drawLesson5Exercise1(canvas,data):
    # draws matrices
    for matrix in data.lesson5Exercise1Matrices: matrix.draw(canvas)
    # draw operation and equal sign
    fontSize = 60
    x,y,font = 400, 300, ("comic sans ms",fontSize,"bold")
    canvas.create_text(x,y,text="+",fill="blue",font=font)
    x,y,font = 600, 300, ("comic sans ms",fontSize,"bold")
    canvas.create_text(x,y,text="=",fill="blue",font=font)

def lesson5Exercise1Check(canvas,data):
    # draw check answer button
    x,y,fontSize = 950,250, 30
    checkAnswer1 = Button(canvas, text="Check Answer",
        highlightbackground="black",
         command=lambda: lesson5CheckAnswer1(data))
    canvas.create_window(x, y, anchor=NE, window=checkAnswer1)
    # draws correct/incorrect:
    if data.lesson5correct1 != None:
        if data.lesson5correct1 == True: text,color = "Correct!","green"
        else: text,color = "Incorrect!", "red"
        x,y,font = 900, 300, ("comic sans ms",fontSize)
        canvas.create_text(x,y,text=text,fill=color,font=font)
    def lesson5CheckAnswer1(data):
        # Changes color to green if correct, red if incorrect
        values1 = data.lesson5Exercise1Matrices[0].values
        values2 = data.lesson5Exercise1Matrices[1].values
        matrix = data.lesson5Exercise1Matrices[2]
        matrix.color = "black"
        try:
            resultingMatrix = addMatrices(values1,values2)
            if matrix.values == resultingMatrix:
                matrix.color, data.lesson5correct1 = "green", True
            else:
                matrix.color, data.lesson5correct1 = "red", False
        except: # crashes due to wrong size
            matrix.color, data.lesson5correct1 = "red", False

def lesson5Exercise2(data): # subtraction exercise
    # sets random size
    minSize, maxSize = 2,3
    rows, cols = random.randint(minSize,maxSize),random.randint(minSize,maxSize)
    # creates first matrix
    values1 = make2dRandomList(rows,cols)
    centerX, centerY = 300, 465
    x,y = topLeftOfMatrix(values1,centerX,centerY)
    data.lesson5Exercise2Matrices.append(Matrix(values1,x,y,None,True))
    # creates second matrix
    values2 = make2dRandomList(rows,cols)
    centerX,centerY = 500, 465
    x,y = topLeftOfMatrix(values2,centerX,centerY)
    data.lesson5Exercise2Matrices.append(Matrix(values2,x,y,None,True))
    # creates modifiable matrix
    horizontalShift = 190
    x,y = x + horizontalShift, y
    data.lesson5Exercise2Matrices.append(Matrix([[1]],x,y,None,False))

def drawLesson5Exercise2(canvas,data):
    # draws matrices
    for matrix in data.lesson5Exercise2Matrices: matrix.draw(canvas)
    # draw operation and equal sign
    fontSize = 60
    x,y,font = 400, 465, ("comic sans ms",fontSize,"bold")
    canvas.create_text(x,y,text="-",fill="blue",font=font)
    x,y,font = 600, 465, ("comic sans ms",fontSize,"bold")
    canvas.create_text(x,y,text="=",fill="blue",font=font)

def lesson5Exercise2Check(canvas,data):
    # draw check answer button
    x,y,fontSize = 950,400, 30
    checkAnswer1 = Button(canvas, text="Check Answer",
        highlightbackground="black",
         command=lambda: lesson5CheckAnswer2(data))
    canvas.create_window(x, y, anchor=NE, window=checkAnswer1)
    # draws correct/incorrect:
    if data.lesson5correct2 != None:
        if data.lesson5correct2 == True: text,color = "Correct!","green"
        else: text,color = "Incorrect!", "red"
        x,y,font = 900, 450, ("comic sans ms",fontSize)
        canvas.create_text(x,y,text=text,fill=color,font=font)
    def lesson5CheckAnswer2(data):
        # Changes color to green if correct, red if incorrect
        values1 = data.lesson5Exercise2Matrices[0].values
        values2 = data.lesson5Exercise2Matrices[1].values
        matrix = data.lesson5Exercise2Matrices[2]
        matrix.color = "black"
        try:
            resultingMatrix = subtractMatrices(values1,values2)
            if matrix.values == resultingMatrix:
                matrix.color, data.lesson5correct2 = "green", True
            else:
                matrix.color, data.lesson5correct2 = "red", False
        except: # crashes due to wrong size
            matrix.color, data.lesson5correct1 = "red", False

def lesson5NewExercise(canvas,data):
    # creates a new exercise by running presets function again
    x,y = 950,550
    newExercise = Button(canvas, text="New problems",
        highlightbackground="black",
         command=lambda: newProblem(data))
    canvas.create_window(x, y, anchor=NE, window=newExercise)
    def newProblem(data):
        # creates new matrices
        lesson5Presets(data)

def lesson5DrawInput(canvas,data):
    # draw typing rectangle
    x,y,width,height = 435,575,130,70
    drawRoundedRectangle(canvas,data,x,y,width,height,"white","blue")
    # draws current input
    x,y = data.width/2, 575
    if data.isTyping == True and data.userInput != "": # user changing number
        canvas.create_text(x,y,text=str(data.userInput), fill="blue", anchor=N,
            font="Times 60")

def lesson5Presets(data): # sets presets for lesson5 and creates exercises
    # wipes memory
    data.lesson5Exercise1Matrices = []
    data.lesson5Exercise2Matrices = []
    data.lesson5correct1 = None
    data.lesson5correct2 = None
    data.selectedObject = None
    data.selectedCell = None
    data.isTyping = False
    data.userInput = ""
    # creates exercises
    lesson5Exercise1(data)
    lesson5Exercise2(data)


####################################
# Lesson 5: Multiplication and Size
####################################

def lesson6KeyPressed(event,data):
    pass

def lesson6TimerFired(data):
    lesson6Presets(data)

def lesson6RedrawAll(canvas,data):
    # draw black background
    canvas.create_rectangle(0,0,data.width,data.height,fill="black")
    drawLessonButtons(canvas,data,"lesson5","lesson7")
    drawLessonTitle(canvas,data,"Multipying Matrices")
    # draw exercise explanation
    fontSize = 30
    x,y,font = data.width/2, 150, ("comic sans ms",fontSize)
    text = """The number of columns of the first matrix must be the same as
the number of rows of the second matrix"""
    canvas.create_text(x,y,text=text,fill="white",font=font)
    # draws example area
    width, height = 600, 350
    x,y = data.width/2 - width/2, 220
    drawRoundedRectangle(canvas,data,x,y,width,height,"white","green")
    # draws example
    lesson6Example(canvas,data)

def lesson6LeftMousePressed(event,canvas,data):
    pass

def lesson6LeftMouseMoved(event,canvas,data):
    pass

def lesson6LeftMouseReleased(event,canvas,data):
    pass

def lesson6RightMousePressed(event,canvas,data):
    pass

def lesson6Example(canvas,data):
    # draw A x B
    fontSize = 50
    x,y,font = 450, 250, ("comic sans ms",fontSize)
    canvas.create_text(x,y,text="A",fill="blue",font=font)
    x,y,font = data.width/2, 250, ("comic sans ms",fontSize)
    canvas.create_text(x,y,text="x",fill="black",font=font)
    x,y,font = 550, 250, ("comic sans ms",fontSize)
    canvas.create_text(x,y,text="B",fill="Red",font=font)
    # draw sizes
    x,y,font = 425, 375, ("comic sans ms",fontSize)
    text = "%d x %d" % (data.lesson6Sizes[0], data.lesson6Sizes[1])
    canvas.create_text(x,y,text=text,fill="blue",font=font)
    # draw sizes
    x,y,font = 575, 375, ("comic sans ms",fontSize)
    text = "%d x %d" % (data.lesson6Sizes[1], data.lesson6Sizes[2])
    canvas.create_text(x,y,text=text,fill="red",font=font)
    # draw arrows
    lesson6DrawArrows(canvas,data)
    # draw size explenations
    fontSize = 20
    x,y,font = data.width/2, 450, ("comic sans ms",fontSize)
    canvas.create_text(x,y,text="These must match",fill="purple",font=font)
    x,y,font = data.width/2, 525, ("comic sans ms",fontSize)
    text = "Resulting matrix will be %d x %d" % \
    (data.lesson6Sizes[0],data.lesson6Sizes[2])
    canvas.create_text(x,y,text=text,fill="orange",font=font)
    
def lesson6DrawArrows(canvas,data):
    # A --> size
    width = 6
    x0,y0,x1,y1 = 450,275,425,350
    canvas.create_line(x0,y0,x1,y1,fill="blue",width=width,arrow=LAST)
    # B --> size
    x0,y0,x1,y1 = 550, 275,575,350
    canvas.create_line(x0,y0,x1,y1,fill="red",width=width,arrow=LAST)
    # draw purple arrows
    x0,y0,x1,y1 = 465, 435, 465, 400
    canvas.create_line(x0,y0,x1,y1,fill="purple",width=width,arrow=LAST)
    x0,y0,x1,y1 = 535, 435, 535, 400
    canvas.create_line(x0,y0,x1,y1,fill="purple",width=width,arrow=LAST)
    x0,y0,x1,y1 = 462, 435, 538, 435
    canvas.create_line(x0,y0,x1,y1,fill="purple",width=width)
    # draw orange arrows
    x0,y0,x1,y1 = 380, 510, 380, 400
    canvas.create_line(x0,y0,x1,y1,fill="orange",width=width,arrow=LAST)
    x0,y0,x1,y1 = 620, 510, 620, 400
    canvas.create_line(x0,y0,x1,y1,fill="orange",width=width,arrow=LAST)
    x0,y0,x1,y1 = 377, 510, 623, 510
    canvas.create_line(x0,y0,x1,y1,fill="orange",width=width)


def lesson6Presets(data): # sets random size for exercise
    minSize, maxSize = 1,5
    data.lesson6Sizes = [random.randint(minSize,maxSize),
                         random.randint(minSize,maxSize),
                         random.randint(minSize,maxSize)]

###################################
# Lesson 7: Multiplying Matrices
###################################

def lesson7KeyPressed(event,data):
    pass

def lesson7TimerFired(data):
    pass

def lesson7RedrawAll(canvas,data):
    # draw black background
    canvas.create_rectangle(0,0,data.width,data.height,fill="black")
    drawLessonButtons(canvas,data,"lesson6","lesson8")
    drawLessonTitle(canvas,data,"Multipying Matrices")
    # draw example explanation
    fontSize = 30
    x,y,font = data.width/2, 150, ("comic sans ms",fontSize)
    text = """To multiply, dot product the rows of the first matrix with
the columns of the second"""
    canvas.create_text(x,y,text=text,fill="white",font=font)
    # draw example
    lesson7DrawExample(canvas,data)
    # draw definition of dot product
    x,y,font = data.width/2, 600, ("comic sans ms",fontSize, "underline")
    text = "The dot product is when you multiply matching elements"
    canvas.create_text(x,y,fill="yellow", text=text, font=font)

def lesson7LeftMousePressed(event,canvas,data):
    pass

def lesson7LeftMouseMoved(event,canvas,data):
    pass

def lesson7LeftMouseReleased(event,canvas,data):
    pass

def lesson7RightMousePressed(event,canvas,data):
    # user can only click resulting matrix
    matrix = data.matrices[2]
    if matrix.matrixContainsClick(event.x,event.y):
        if findMatrixCell(matrix,event.x,event.y) != None:
            (row,col) = findMatrixCell(matrix,event.x,event.y)
            data.selectedCell = (row,col)
            matrix.highlightedValues = [(row,col)]
            # highlights row in first matrix
            data.matrices[0].highlightedValues = []
            for j in range(len(data.matrices[0].values[0])):
                data.matrices[0].highlightedValues.append((row,j))
            # highlights column in second matrix
            data.matrices[1].highlightedValues = []
            for i in range(len(data.matrices[1].values)):
                data.matrices[1].highlightedValues.append((i,col))
        if data.selectedCell != None:
            data.lesson7Text = lesson7MakeEquation(data)

def lesson7DrawExample(canvas,data):
    # draws example area
    width, height = 600, 350
    x,y = data.width/2 - width/2, 220
    drawRoundedRectangle(canvas,data,x,y,width,height,"white","green")
    #draw matrices
    for matrix in data.matrices: matrix.draw(canvas)
    # draws multiplication and equal sign
    fontSize = 60
    x,y,font = 400, data.height/2, ("comic sans ms",fontSize,"bold")
    canvas.create_text(x,y,text="x",fill="blue",font=font)
    x,y,font = 600, data.height/2, ("comic sans ms",fontSize,"bold")
    canvas.create_text(x,y,text="=",fill="blue",font=font)
    # draws equation for value
    if data.lesson7Text != "":
        fontSize = 30
        x,y,font = data.width/2, 500, ("comic sans ms",fontSize,"bold")
        canvas.create_text(x,y,text=data.lesson7Text,fill="blue",font=font)
    lesson7NewExercise(canvas,data)
    # draw highlight explanation
    fontSize,lineWidth = 20, 6
    x,y,font = 420, 275, ("comic sans ms",fontSize)
    text = """Right click the entries to see how this works"""
    canvas.create_text(x,y,text=text,fill="blue",font=font)
    # draw arrows for highlight explanation
    x0,y0,x1,y1 = 635,275,703,275
    canvas.create_line(x0,y0,x1,y1,fill="blue",width=lineWidth)
    x0,y0,x1,y1 = 700,275,700,300
    canvas.create_line(x0,y0,x1,y1,fill="blue",width=lineWidth,arrow=LAST)

def lesson7MakeEquation(data):
    # returns string of equation for how selected value was made
    result = ""
    matrixA,matrixB,matrixC = data.matrices[0],data.matrices[1],data.matrices[2]
    row,col = data.selectedCell
    # gets elements of rows from matrix A and cols from Matrix B
    rowList = matrixA.values[row]
    colList = []
    for i in range(len(matrixB.values)):
        colList.append(matrixB.values[i][col])
    for x in range(len(rowList)): # starts forming string
        result += "(%d)(%d) + " % (rowList[x], colList[x])
    # cuts off last "+" and adds result
    index = -2
    result = result[:index] + "= %d" % (matrixC.values[row][col])
    return result


def lesson7NewExercise(canvas,data):
    # creates a new exercise by running presets function again
    x,y = 950,375
    newExercise = Button(canvas, text="New Example",
        highlightbackground="black",
         command=lambda: newProblem(data))
    canvas.create_window(x, y, anchor=NE, window=newExercise)
    def newProblem(data):
        # creates new matrices
        lesson7Presets(data)


def lesson7Presets(data):
    data.matrices = []
    data.lesson7Text = ""
    minSize,maxSize = 1,3
    rows,cols = random.randint(minSize,maxSize),random.randint(minSize,maxSize)
    # creates first matrix
    values1 = make2dRandomList(rows,cols)
    centerX,centerY = 300, data.height/2
    x,y = topLeftOfMatrix(values1,centerX,centerY)
    data.matrices.append(Matrix(values1,x,y,None,True))
    # creates second matrix
    rows, cols = cols, random.randint(minSize,maxSize)
    values2 = make2dRandomList(rows,cols)
    centerX,centerY = data.width/2, data.height/2
    x,y = topLeftOfMatrix(values2,centerX,centerY)
    data.matrices.append(Matrix(values2,x,y,None,True))
    # creates resulting matrix
    values3 = multiplyMatrices(values1,values2)
    centerX,centerY = 700, data.height/2
    x,y = topLeftOfMatrix(values3,centerX,centerY)
    data.matrices.append(Matrix(values3,x,y,None,False))

#####################################
# Lesson 8: Multiplication Exercises
#####################################

def lesson8KeyPressed(event,data):
    if data.selectedObject != None and data.isTyping == False: 
        # changes size of select matrix
        if event.keysym == "Up": data.selectedObject.deleteRow()
        elif event.keysym == "Down": data.selectedObject.addRow()
        elif event.keysym == "Left": data.selectedObject.deleteCol()
        elif event.keysym == "Right": data.selectedObject.addCol()
    else:
        if data.isTyping == True: # records user input
            lesson8UserTyping(event,data)

def lesson8UserTyping(event,data):
    if event.keysym == "Return": # user finishes typing
        # changes matrix cell
        row,col = data.selectedCell
        if data.userInput != "":
            try:
                data.selectedObject.values[row][col]=int(data.userInput)
            except: # ignores input if causes error
                pass
        data.selectedObject.highlightedValues = []
        data.userInput = ""
        data.isTyping = False
        data.selectedObject = None
    else: # user adds a number
        if event.keysym.isdigit():
            data.userInput += event.keysym
        elif event.keysym == "minus": #adds a negative sign
            data.userInput = "-" + data.userInput

def lesson8TimerFired(data):
    pass

def lesson8RedrawAll(canvas,data):
    # draw black background
    canvas.create_rectangle(0,0,data.width,data.height,fill="black")
    drawLessonButtons(canvas,data,"lesson7","lesson9")
    drawLessonTitle(canvas,data,"Try this exercise!")
    # draws example area
    width, height = 600, 400
    x,y = data.width/2 - width/2, 150
    drawRoundedRectangle(canvas,data,x,y,width,height,"white","green")
    # draws dashed selection
    if data.selectedObject != None:
        data.selectedObject.drawDash(canvas)
    # draws user input
    lesson8DrawInput(canvas,data)
    # draws exercises
    drawLesson8Exercise1(canvas,data)
    drawLesson8Exercise2(canvas,data)
    # draws Exercise buttons
    lesson8Exercise1Check(canvas,data)
    lesson8Exercise2Check(canvas,data)
    # draws new exercise button
    lesson8NewExercise(canvas,data)
    # draws dashed selection
    if data.selectedObject != None:
        data.selectedObject.drawDash(canvas)

def lesson8LeftMousePressed(event,canvas,data):
    clickedOnObject = False
    if data.isTyping == False: # locks user out if he's not typing
        for matrix in data.lesson8Exercise1Matrices:
            if matrix.matrixContainsClick(event.x,event.y) and \
                matrix.locked == False: 
                data.selectedObject = matrix
                clickedOnObject = True
        for matrix in data.lesson8Exercise2Matrices:
            if matrix.matrixContainsClick(event.x,event.y) and \
                matrix.locked == False:
                data.selectedObject = matrix
                clickedOnObject = True
        # unselects object if clicked on empty space
        if clickedOnObject == False and event.x > data.workspaceSideBarWidth:
            data.selectedObject = None

def lesson8LeftMouseMoved(event,canvas,data):
    pass

def lesson8LeftMouseReleased(event,canvas,data):
    pass

def lesson8RightMousePressed(event,canvas,data):
    if data.isTyping == False:
        clickedOnObject = False
        # selects matrix if clicked on
        if lesson8RightMousePressedMatrix(event,canvas,data):
            clickedOnObject = True
        # unselects object if clicked on empty space
        if clickedOnObject == False and event.x > data.workspaceSideBarWidth:
            data.selectedObject = None

def lesson8RightMousePressedMatrix(event,canvas,data):
    # returns true if matrix is clicked and highlights cell
    for matrix in data.lesson8Exercise1Matrices:
        if matrix.matrixContainsClick(event.x,event.y) and \
            matrix.locked == False:
            if findMatrixCell(matrix,event.x,event.y) != None:
                data.selectedObject = matrix
                (row,col) = findMatrixCell(matrix,event.x,event.y)
                data.selectedCell = (row,col)
                matrix.highlightedValues.append((row,col)) # highlight cell
                clickedOnObject,data.isTyping = True, True
                return True
    for matrix in data.lesson8Exercise2Matrices:
        if matrix.matrixContainsClick(event.x,event.y) and \
            matrix.locked == False:
            if findMatrixCell(matrix,event.x,event.y) != None:
                data.selectedObject = matrix
                (row,col) = findMatrixCell(matrix,event.x,event.y)
                data.selectedCell = (row,col)
                matrix.highlightedValues.append((row,col)) # highlight cell
                clickedOnObject, data.isTyping = True, True
                return True
        

def lesson8DrawInput(canvas,data):
    # draw typing rectangle
    x,y,width,height = 435,575,130,70
    drawRoundedRectangle(canvas,data,x,y,width,height,"white","blue")
    # draws current input
    x,y = data.width/2, 575
    if data.isTyping == True and data.userInput != "": # user changing number
        canvas.create_text(x,y,text=str(data.userInput), fill="blue", anchor=N,
            font="Times 60")

def lesson8Exercise1(data): # addition exercse
    # sets random size for matrix 1
    minSize, maxSize = 2,3
    rows1,cols1=random.randint(minSize,maxSize),random.randint(minSize,maxSize)
    # creates first matrix
    values1 = make2dRandomList(rows1,cols1)
    centerX, centerY = 530, 250
    x,y = topLeftOfMatrix(values1,centerX,centerY)
    data.lesson8Exercise1Matrices.append(Matrix(values1,x,y,None,True))
    # creates second matrix
    rows2,cols2=random.randint(minSize,maxSize),random.randint(minSize,maxSize)
    values2 = make2dRandomList(rows2,cols2)
    centerX,centerY = 675, 250
    x,y = topLeftOfMatrix(values2,centerX,centerY)
    data.lesson8Exercise1Matrices.append(Matrix(values2,x,y,None,True))
    # stores correct answer
    data.lesson8Answer1 = (cols1 == rows2)

def drawLesson8Exercise1(canvas,data):
    # draws matrices
    for matrix in data.lesson8Exercise1Matrices: matrix.draw(canvas)
    # draw question
    fontSize = 20
    x,y, font = 450, 250, ("comic sans ms",fontSize)
    text = "Can you multiply \n these two matrices?"
    canvas.create_text(x,y,text=text,font=font,anchor=E)
   
def lesson8Exercise1Check(canvas,data):
    # draw Yes button
    x,y = 900,225
    checkAnswer1 = Button(canvas, text="Yes",
        highlightbackground="black",
         command=lambda: lesson8CheckAnswer1(data,True))
    canvas.create_window(x, y, window=checkAnswer1)
    # draw No button
    x,y = 900,250
    checkAnswer2 = Button(canvas, text="No",
        highlightbackground="black",
         command=lambda: lesson8CheckAnswer1(data,False))
    canvas.create_window(x, y, window=checkAnswer2)
    # draws correct/incorrect:
    if data.lesson8correct1 != None:
        if data.lesson8correct1 == True: text,color = "Correct!","green"
        else: text,color = "Incorrect!", "red"
        fontSize = 30
        x,y,font = 900, 300, ("comic sans ms",fontSize)
        canvas.create_text(x,y,text=text,fill=color,font=font)
    def lesson8CheckAnswer1(data,response):
        # changes data wether response is correct or not
        data.lesson8correct1 = (data.lesson8Answer1 == response)


def lesson8Exercise2(data): # subtraction exercise
    # sets random size
    minSize,maxSize = 1,3
    rows, cols = random.randint(minSize,maxSize),random.randint(minSize,maxSize)
    # creates first matrix
    values1 = make2dRandomList(rows,cols)
    centerX, centerY = 300, 465
    x1,y1 = topLeftOfMatrix(values1,centerX,centerY)
    data.lesson8Exercise2Matrices.append(Matrix(values1,x1,y1,None,True))
    # creates second matrix
    rows, cols = cols, random.randint(minSize,maxSize)
    values2 = make2dRandomList(rows,cols)
    centerX, centerY = data.width/2, 465
    x2,y2 = topLeftOfMatrix(values2,centerX,centerY)
    data.lesson8Exercise2Matrices.append(Matrix(values2,x2,y2,None,True))
    # creates modifiable matrix
    horizontalShift = 190
    x,y = x2 + horizontalShift, y1
    data.lesson8Exercise2Matrices.append(Matrix([[1]],x,y,None,False))


def drawLesson8Exercise2(canvas,data):
    # draws matrices
    for matrix in data.lesson8Exercise2Matrices: matrix.draw(canvas)
    # draw operation and equal sign
    fontSize = 60
    x,y,font = 400, 465, ("comic sans ms",fontSize,"bold")
    canvas.create_text(x,y,text="x",fill="blue",font=font)
    x,y,font = 600, 465, ("comic sans ms",fontSize,"bold")
    canvas.create_text(x,y,text="=",fill="blue",font=font)


def lesson8Exercise2Check(canvas,data):
    # draw check answer button
    x,y = 950,400
    checkAnswer = Button(canvas, text="Check Answer",
        highlightbackground="black",
         command=lambda: lesson8CheckAnswer2(data))
    canvas.create_window(x, y, anchor=NE, window=checkAnswer)
    # draws correct/incorrect:
    if data.lesson8correct2 != None:
        if data.lesson8correct2 == True: text,color = "Correct!","green"
        else: text,color = "Incorrect!", "red"
        fontSize = 30
        x,y,font = 900, 450, ("comic sans ms",fontSize)
        canvas.create_text(x,y,text=text,fill=color,font=font)
    def lesson8CheckAnswer2(data):
        # Changes color to green if correct, red if incorrect
        values1 = data.lesson8Exercise2Matrices[0].values
        values2 = data.lesson8Exercise2Matrices[1].values
        matrix = data.lesson8Exercise2Matrices[2]
        matrix.color = "black"
        try:
            resultingMatrix = multiplyMatrices(values1,values2)
            if matrix.values == resultingMatrix:
                matrix.color, data.lesson8correct2 = "green", True
            else:
                matrix.color, data.lesson8correct2 = "red", False
        except: # crashes due to wrong size
            matrix.color, data.lesson8correct1 = "red", False

def lesson8NewExercise(canvas,data):
    # creates a new exercise by running presets function again
    x,y = 950,500
    newExercise = Button(canvas, text="New problems",
        highlightbackground="black",
         command=lambda: newProblem(data))
    canvas.create_window(x, y, anchor=NE, window=newExercise)
    def newProblem(data):
        # creates new matrices
        lesson8Presets(data)

def lesson8Presets(data):
    # wipes memory
    data.lesson8Exercise1Matrices = []
    data.lesson8Exercise2Matrices = []
    data.lesson8correct1 = None
    data.lesson8correct2 = None
    data.selectedObject = None
    data.selectedCell = None
    data.isTyping = False
    data.userInput = ""
    # creates exercises
    lesson8Exercise1(data)
    lesson8Exercise2(data)


#################################
# Lesson 9: Finished Course
#################################

def lesson9KeyPressed(event,data):
    pass

def lesson9TimerFired(data):
    pass

def lesson9RedrawAll(canvas,data):
    # draw black background
    canvas.create_rectangle(0,0,data.width,data.height,fill="black")
    fontSize = 60
    x,y,font = data.width/2,250,("comic sans ms",fontSize,"bold")
    text = "Congratulations!"
    canvas.create_text(x,y,text=text,font=font, fill="green")
    fontSize = 30
    x,y,font = data.width/2,data.height/2,("comic sans ms",fontSize)
    text = "You now know the basics of Matrix algebra!"
    canvas.create_text(x,y,text=text,font=font, fill="green")
    lesson9DrawButtons(canvas,data)

def lesson9LeftMousePressed(event,canvas,data):
    pass

def lesson9LeftMouseMoved(event,canvas,data):
    pass

def lesson9LeftMouseReleased(event,canvas,data):
    pass

def lesson9RightMousePressed(event,canvas,data):
    pass

def lesson9DrawButtons(canvas,data):
    # draw Main screen button
    x,y,width,height = 325, 495, 150, 40
    drawRoundedRectangle(canvas,data,x,y,width,height,"red","red")
    x,y = 450, 500 
    mainScreen = Button(canvas, text="Main Screen",highlightbackground="red",
         command=lambda: changeSplashScreen("mainScreen",data))
    canvas.create_window(x, y, anchor=NE, window=mainScreen)
    # draw exit button
    x,y,width,height = 525, 495, 150, 40
    drawRoundedRectangle(canvas,data,x,y,width,height,"blue","blue")
    x,y = 550, 500 
    workspace = Button(canvas, text="Workspace",highlightbackground="blue",
         command=lambda: changeSplashScreen("workspace",data))
    canvas.create_window(x, y, anchor=NW, window=workspace)


#################################
# Lessons Functions
#################################

def make2dRandomList(rows, cols):
    # taken from notes
    # creates a 2d list with size rows x cols and random entries
    a=[]
    entryMin, entryMax = -3, 5
    for row in range(rows):
        a.append([])
        for col in range(cols):
            a[row].append(random.randint(entryMin, entryMax))
    return a

def drawLessonButtons(canvas,data,backScreen,nextScreen):
    # draw exit button
    x,y = data.width,5 
    mainScreen = Button(canvas, text="Exit",highlightbackground="black",
         command=lambda: changeSplashScreen("mainScreen",data))
    canvas.create_window(x, y, anchor=NE, window=mainScreen)

    # draw back button
    x,y, width, height = 350, 680, 100, 50
    drawRoundedRectangle(canvas,data,x,y,width,height,"red","red")
    horizontalShift,verticalShift = 20, 25
    x,y = x + horizontalShift, y + verticalShift
    backButton = Button(canvas, text="Back",highlightbackground="red",
         command=lambda: changeSplashScreen(backScreen,data))
    canvas.create_window(x, y, anchor=W, window=backButton)

    # draw next button
    x,y, width, height = 550, 680, 100, 50
    drawRoundedRectangle(canvas,data,x,y,width,height,"green","green")
    x,y = x + horizontalShift, y + verticalShift
    nextButton = Button(canvas, text="Next",highlightbackground="green",
         command=lambda: changeSplashScreen(nextScreen,data))
    canvas.create_window(x, y, anchor=W, window=nextButton)

def drawLessonTitle(canvas,data,title):
    # draws lesson title inside rounded rectangle
    factor = 30
    width, height = len(title)*factor, 65
    x, y = data.width/2 - width/2, 30
    drawRoundedRectangle(canvas,data,x,y,width,height,"black","green")
    x, y,fontSize = data.width/2, 60, 50
    canvas.create_text(x,y,text=title,fill="green",
        font=("comic sans ms",fontSize, "bold"))

def topLeftOfMatrix(values,x,y):
    # given a matrix in a 2d list and values, determines top left for matrix
    # so matrix is centered at x,y
    rows = len(values)
    cols = len(values[0])
    margin = 10
    numberSep = 20
    numberWidth = getNumberWidth(values)
    factor = 1.5
    matrixWidth = margin*factor + numberWidth*cols + numberSep*(cols-1)
    matrixHeight = margin*2 + numberWidth*rows + numberSep*(rows-1)
    return (x - matrixWidth/2, y - matrixHeight/2)

def addMatrices(values1,values2):
    # add two matrices and return resulting matrix
    result = make2dList(len(values1),len(values1[0]))
    for i in range(len(result)):
        for j in range(len(result[0])):
            result[i][j] = values1[i][j]+values2[i][j]
    return result

def subtractMatrices(values1,values2):
    # subtract two matrices and return resulting matrix
    result = make2dList(len(values1),len(values1[0]))
    for i in range(len(result)):
        for j in range(len(result[0])):
            result[i][j] = values1[i][j] - values2[i][j]
    return result

def multiplyMatrices(values1,values2):
    # multiplies two matrices given their 2d lists of values
    result = np.matmul(values1,values2)
    # convert to 2d list
    result = list(result)
    for row in range(len(result)):
        result[row] = list(result[row])
    return result


####################################
# Run function
# taken from notes
####################################


def rgbString(red, green, blue): # taken from notes
    return "#%02x%02x%02x" % (red, green, blue)


def run(width=1000, height=750):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    def leftMousePressedWrapper(event,canvas,data):
        leftMousePressed(event,canvas,data)
        #redrawAllWrapper(canvas,data)

    def rightMousePressedWrapper(event,canvas,data):
        rightMousePressed(event,canvas,data)
        redrawAllWrapper(canvas,data)

    def leftMouseMovedWrapper(event,canvas,data):
        leftMouseMoved(event,canvas,data)
        redrawAllWrapper(canvas,data)

    def leftMouseReleasedWrapper(event,canvas,data):
        leftMouseReleased(event,canvas,data)
        redrawAllWrapper(canvas,data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 5000 # milliseconds
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    #sets up data
    init(data,canvas)
    # mouse presses
    canvas.bind("<Motion>", lambda event: mouseMotion(event,data))
    root.bind("<Button-1>", lambda event:
                                leftMousePressedWrapper(event,canvas,data))
    root.bind("<Button-2>", lambda event:
                                rightMousePressedWrapper(event,canvas,data))
    canvas.bind("<B1-Motion>", lambda event:
                                leftMouseMovedWrapper(event,canvas,data))
    root.bind("<B1-ButtonRelease>", lambda event:
                                leftMouseReleasedWrapper(event,canvas,data))
    # key presses
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))

    # timer fired
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed

run()

def testAddMatrices():
    print("Testing addMatrices...",end="")
    matrixA = [[2,3]]
    matrixB = [[3,4]]
    assert(addMatrices(matrixA,matrixB) == [[5,7]])
    matrixA = [[2]]
    matrixB = [[-2]]
    assert(addMatrices(matrixA,matrixB) == [[-0]])
    matrixA = [[1,0],[0,1]]
    matrixB = [[2,2],[2,2]]
    assert(addMatrices(matrixA,matrixB) == [[3,2],[2,3]])
    print("Passed!")

def testSubtractMatrices():
    print("Testing subtractMatrices...",end="")
    matrixA = [[2,3]]
    matrixB = [[3,4]]
    assert(subtractMatrices(matrixA,matrixB) == [[-1,-1]])
    matrixA = [[2]]
    matrixB = [[-2]]
    assert(subtractMatrices(matrixA,matrixB) == [[4]])
    matrixA = [[1,0],[0,1]]
    matrixB = [[2,2],[2,2]]
    assert(subtractMatrices(matrixA,matrixB) == [[-1,-2],[-2,-1]])
    print("Passed!")

def testMultiplyMatrices():
    print("Testing multiplyMatrices...",end="")
    matrixA = [[2,3]]
    matrixB = [[1],[1]]
    assert(multiplyMatrices(matrixA,matrixB) == [[5]])
    matrixA = [[2]]
    matrixB = [[-2]]
    assert(multiplyMatrices(matrixA,matrixB) == [[-4]])
    matrixA = [[1,0],[0,1]]
    matrixB = [[2,2],[2,2]]
    assert(multiplyMatrices(matrixA,matrixB) == [[2,2],[2,2]])
    print("Passed!")

testAddMatrices()
testSubtractMatrices()
testMultiplyMatrices()


