import numpy as np

Depth = 1;
class State:
    def __init__(self, state, directionFlag=None, parent=None,depth = 1):
        self.state = state
        # state is a ndarray with a shape(3,3) to storage the state
        self.direction = ['up', 'down', 'right', 'left']
        if directionFlag:
            self.direction.remove(directionFlag)
        # record the possible directions to generate the sub-states
        self.parent = parent
        self.depth = 1

    def showInfo(self):
        for i in range(3):
            for j in range(3):
                print(self.state[i, j], end='  ')
            print("\n")
        print('->')
        return

    def getEmptyPos(self):
        postion = np.where(self.state == self.symbol)
        return postion

    def generateSubStates(self):  # 产生子节点
        if not self.direction:
            return []
        subStates = []
        boarder = len(self.state) - 1
        # the maximum of the x,y
        row, col = self.getEmptyPos()
        if 'left' in self.direction and col > 0:  # 向左移动
            s = self.state.copy()
            # 标志位symbol=0向左移动，产生新的状态节点，加入到subStates中

            temp = s.copy()
            s[row, col] = s[row, col - 1]
            s[row, col - 1] = temp[row, col]
            news = State(s, directionFlag='right', parent=self)
            subStates.append(news)

        if 'up' in self.direction and row > 0:
            s = self.state.copy()
            # 标志位symbol=0向上移动，产生新的状态节点，加入到subStates中

            temp = s.copy()
            s[row, col] = s[row - 1, col]
            s[row - 1, col] = temp[row, col]
            news = State(s, directionFlag='down', parent=self)
            subStates.append(news)

        if 'down' in self.direction and row < boarder:  # it can move to down place
            s = self.state.copy()
            # 标志位symbol=0向下移动，产生新的状态节点，加入到subStates中

            temp = s.copy()
            s[row, col] = s[row + 1, col]
            s[row + 1, col] = temp[row, col]
            news = State(s, directionFlag='up', parent=self)
            subStates.append(news)

        if self.direction.count('right') and col < boarder:  # it can move to right place
            s = self.state.copy()
            # 标志位symbol=0向右移动，产生新的状态节点，加入到subStates中

            temp = s.copy()
            s[row, col] = s[row, col + 1]
            s[row, col + 1] = temp[row, col]
            news = State(s, directionFlag='left', parent=self)
            subStates.append(news)

        # end1
        return subStates

    def BFS(self):
        # generate a empty openTable
        openTable = []  # 存放状态的地方
        path = [] # 存放答案的地方
        # append the origin state to the openTable
        openTable.append(self)  # 将初始状态加入
        steps = 1  # 步骤
        seen = []
        while len(openTable) > 0 :
            n = openTable.pop(0)  # pop() 函数用于移除列表中的一个元素（默认最后一个元素），并且返回该元素的值。
            subStates = n.generateSubStates()
            seen.append(n);
            steps = steps + 1;  # 每展开一个节点，步骤+1
            # 查看子状态中有没有最终状态，如果有则输出之前的父状态到path中，输出step+1
            ###########开始1#############
            for subState in subStates :
                if (subState.state == State.answer).all():
                    subState = subState.parent
                    #通过父节点不断追溯寻找父节点，直到找到最初结点
                    while(subState.state != s1.state).any() :
                        path.append(subState);
                        subState = subState.parent;
                    path.reverse();
                    return path,steps
            ###########结束1#############

            # 将子状态添加到openTable中
            ###########开始2#############
                if subState not in seen:
                    openTable.append(subState);
            ###########结束2#############
        else:
            return None, None

State.symbol = 0
State.answer = np.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]])
s1 = State(np.array([[2, 8, 3], [1, 6, 4], [7, 0, 5]]))
path, steps = s1.BFS()
if path:  # if find the solution
    for node in path:
        # print the path from the origin to final state
        node.showInfo()
    print(State.answer)
    print("Total steps is %d" % steps)
