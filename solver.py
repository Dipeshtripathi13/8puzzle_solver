from cmath import inf
import copy
import pygame
from config import goal, initial, backgroundColor, screen_size
from draw_util import Drawer



screen = pygame.display.set_mode(screen_size) # w, h

pygame.display.set_caption('8 Puzzle Solver')
screen.fill(backgroundColor)

pygame.init()
font = pygame.font.SysFont('Times', 15)
running = True


# def draw_state(screen, state, pos, text): # state is 3x3 mat
#     global font
#     w = 60
#     h= 60
#     for i, column in zip(state, range(3)):
#         for count, row in zip(i, range(3)):
#             x = pos[0]+w*row
#             y = pos[1]+h*column
#             rectangle_ = pygame.Rect(x, y, w, h)
#             pygame.draw.rect(screen, ((count*15)%255, 0, 0), rectangle_)
#             del rectangle_
#             screen.blit(font.render(str(count%9), True, (255,255,255)), (x+w/2, y+h/2))
#             pygame.display.update()

#     i = screen.blit(font.render(text, True, (0,0,0)), (pos[0], pos[1]-h))
#     del i

    

class Solver:
    def __init__(self, initialState, finalState, screen, events):
        self.initial = initialState
        self.goal = finalState
        self.traversedState_ = []
        self.stack = []
        self.costStack = []
        self.minCost = inf
        self.screen = screen
        self.events = events
        self.totalSteps = 0
        
        self.solve(self.initial, self.goal)


    def cost(self, toCompareMat):
        result = 0
        for rowIndex in range(len(self.goal)):
            for columnIndex in range(len(self.goal[rowIndex])):
                if self.goal[rowIndex][columnIndex] != toCompareMat[rowIndex][columnIndex]:
                    (goalRowIndex, goalColumnIndex) = self.index_2d(self.goal, toCompareMat[rowIndex][columnIndex])
                    rowChange = abs(goalRowIndex - rowIndex)
                    columnChange = abs(goalColumnIndex - columnIndex)
                    result += rowChange + columnChange
        return result


    def print_matrix(self, mat, sep = ' '):
        a = [i for i in mat]
        
        while(len(a)<10):
            a.append([
                [' ', ' ', ' '],
                [' ', ' ', ' '],
                [' ', ' ', ' '],
            ])
        for i in zip(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9]): # four possibilities are present 
            for row in i:
                if ' ' not in row:
                    print(row, end=sep)      
            print('')


    def index_2d(self, myList, v):
        for i, x in enumerate(myList):  # Find what the hell is this first
            if v in x:
                return i, x.index(v)

    def next_steps(self, mat, p=True, checkAlready =True):
        global running
                
        if mat in self.traversedState_ and checkAlready:
            return 'Already traversed'
        if p:
            print('Current Matrix:')
            self.print_matrix([mat])
            drawer.draw_state(mat, (50, 600/2 + 80), 'SOLVING')
            for event in self.events:
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
        
        self.traversedState_.append(copy.deepcopy(mat))
        if p:
            print('Next Steps')
        emptyPosition = self.index_2d(mat, 0)
        result, hs, offsets = [], [], [1, -1, 0]
        orgMat = copy.deepcopy(mat)
        
        for x in offsets:
            for y in offsets:
                if abs(x + y) == 1:
                    newX = emptyPosition[0] + x
                    newY = emptyPosition[1] + y
                    if 0 <= newX <= 2 and  0 <= newY <= 2:
                    
                        mat[emptyPosition[0]][emptyPosition[1]] = mat[newX][newY]
                        mat[newX][newY] = 0
                        if mat not in self.traversedState_ and mat != [
                                [1, 2, 3],
                                [4, 5, 6],
                                [8, 7, 0]
                                ]:
                            result.append(mat)
                            self.stack.append(mat)
                            c = self.cost(copy.deepcopy(mat))
                            if p:
                                print(f'Cost: {c}', end='\t')
                            self.costStack.append(c)
                        
                        mat = copy.deepcopy(orgMat)
        if p:
            print('')
        return result


    def check_traversed(self):
        step = 0
        temp = []
        for i in range(1, len(self.traversedState_)+1):
            lastTraversed = self.traversedState_[-i:][0]
                
            if initial in self.next_steps(lastTraversed, False, False):
                self.print_matrix(temp)
                return step
            temp.append(lastTraversed)

    
    def solve(self, initial, goal):
        step = 0  
        while(initial != goal):
            step += 1
            print(f'\nStep: {step}\n')
            res = self.next_steps(initial)
            self.print_matrix(res)
            
            i = self.costStack.index((min(self.costStack)))
            temp = self.costStack.pop(i)
            if temp<self.minCost:
                self.minCost = temp
            
            print(f'Minimum cost till now: {self.minCost}')
            print(f'Stack size: {len(self.stack)}')
            
            initial = self.stack.pop(i)    
            
            
            if step > 40000:
                break
            

        print(f'\nTraversed States:')
        self.traversedState_.append(self.goal)
        drawer.draw_state(self.goal, (50, 600/2 + 80), '')
        

        for matIndex in range(0, len(self.traversedState_), 10):
            self.print_matrix(self.traversedState_[matIndex:matIndex+10])
            print("")
        
        print(f'\nSummary:\n\tSteps: {step}')
        self.totalSteps = step

#pygame window creation
drawer = Drawer(screen, font)
drawer.drawActual((50, 100))

drawer.draw_state(initial, (600/2 + 50, 100), 'INITIAL STATE')

#split the window in four half

pygame.draw.line(screen, (0, 0, 0), (600/2, 0), (600/2, 600), width=1)
pygame.draw.line(screen, (0, 0, 0), (0, 600/2), (600, 600/2), width=1)


pygame.display.update()
runSolver = True
traversedStateIndex = 0
if __name__ == '__main__':
    while running:
        events = pygame.event.get()
        for event in events:
            if not runSolver:
                drawer.draw_state(S1.traversedState_[traversedStateIndex%len(S1.traversedState_)], (600/2 + 50, 600/2 + 90), 'Starts from initial state' )
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key in [pygame.K_UP, pygame.K_w]:
                    traversedStateIndex += 1
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    traversedStateIndex -= 1
        if runSolver:
            S1 = Solver(initial, goal, screen, events)
            screen.blit(font.render('Total Steps: ' + str(S1.totalSteps), True, (0,0,0)), (600/2 + 50, 600/2+10))
            pygame.display.update()
            drawer.draw_state(S1.traversedState_[traversedStateIndex%len(S1.traversedState_)], (600/2 + 50, 600/2 + 90), 'Starts from initial state' )
            screen.blit(font.render('Press arrow button to increase/decrease', True, (0,0,0)), (600/2 + 50, 600/2+50))
            pygame.display.update()
            runSolver = False
            
            
        