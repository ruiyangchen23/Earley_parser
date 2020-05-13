# note: not tested yet
from collections import defaultdict
class parser:
    def __init__(self,root, input_string, non_terminal_list, terminal_list):
        # root should be a non terminal 
        self.root = root
        self.input_string = input_string
        #  3d struture, a array of hashmap, whose value points to a set. 
        self.states = []
        # state[i][key] should look like set([RR.AA,A,2,j]) 2 is the position of the dot, A is the key 
        self.non_terminal_mapping = {}
        self.terminals = set(terminal_list)
        for non_terminal in non_terminal_list:
            self.non_terminal_mapping[non_terminal.symbol] = non_terminal
         
        return 
    # expand current state, try to explore all the rules that applicable (we don't trim yet)
    def predict(self, state_list,k):
        new_set = set()
        for state in state_list:
            #  K: left-> [RR.AA: partial_parsing,A: next_symbol,2: dot_index,j:j ]
            left , partial_parsing, _, dot_index, j = state
            if dot_index==len(partial_parsing):
                updates = self.complete(None,k)
                new_set += updates
            else:
                next_symbol = partial_parsing[dot_index]
                if next_symbol in self.terminals:
                    term = self.terminals[next_symbol]
                    for expandable in term.rhs:
                        new_left, new_partial, first, new_dot_index, new_j = term.left, expandable, expandable[0], 0, k
                        new_item =(new_left, new_partial, first, new_dot_index, new_j)
                        if self.instate(k,new_item):
                            new_set.add(new_item)
                            self.states[k][first].add(new_item);
                else:
                    if next_symbol == self.input_string[k]:
                        # either move to next position or parsing
                        new_left ,new_partial, new_symbol, new_dot_index, new_j = left,partial_parsing, partial_parsing[dot_index+1], dot_index+1, j
                        new_item = (new_left ,new_partial, new_symbol, new_dot_index, new_j)
                        if not self.instate(k,new_item):
                            new_set.add(new_item)
                            self.states[k][new_symbol].add(new_item)
                    #  check if it match, if match then complete, else no
                        # add next symbol and it's rule to the state. merge 2 sets i guess? and recursively call on new symbols
        return new_set

    def instate(self,k,left, partial,symbol, dot_index, j):
        if symbol in self.states[k]:
            if (left,partial,symbol,dot_index,j) in self.states[k][symbol]:
                return True
        return False

    # check for next symbol, and possible advance some terminals
    def scan(self,k):
        kplus1 = k+1
        next_symbol = self.input_string[k+1]
        for state in self.states[k]:
            # we made sure it's a terminal in this step. 
            if next_symbol in state:
                for v in state[next_symbol]:
                    left, partial_parsing, _, dot_index, j = v
                    # should dot_index<= len(partial_parsing)?? 
                    next_key = partial_parsing[dot_index+1]
                    self.states[kplus1][next_key].add( (left,partial_parsing,next_key,dot_index+1,j))
        pass   
    
    # recursive complete
    # should record left 
    def complete(self,k, left, partial, dot_index, j):
        if dot_index<=len(partial):
            print ('error! not complete! ')
            return set()
        newset = set()
        for state in self.states[j][left]:
            # prev_symbol should == left
            prev_left, prev_partial, prev_symbol, prev_dot_index, prev_j = state
            next_left = prev_left
            next_partial = prev_partial
            next_dot_index = prev_dot_index+1
            next_symbol = prev_left[next_dot_index]
            next_j = prev_j
            new_item = (next_left,next_partial,next_symbol,next_dot_index,next_j)
            if not self.instate(k,new_item):
                newset.add( new_item)
                self.states[k][next_symbol].add( new_item)
        return newset


    def parse(self):
        length = len(self.input_string)
        for i in range(length):
            self.states.append(defaultdict(lambda: set()))
        root = self.root
        left = root.left
        rhs = root.rhs
        # new_set = set()
        #  todo: probably should start in -1 instead. 
        for right in rhs:
            self.states[0][right[0]].add((left,right,right[0],0,0))
            # new_set.add((left,right,right[0],0,0))
        for k in range(length):
            curr_set = set()
            for k,states in self.states[k].items():
                for state in states:
                    curr_set.add(state)
            while (len(curr_set)>0):
                curr_set = self.predict(curr_set,k)
            self.scan(k)
        # then for 
        last = self.states[-1]
        if self.root.left in last:
            return last[self.root.left]
        else:
            print ("None parsing tree found")
            return None

class non_terminal:
    def __init__(self,left, rhs):
        self.left = left
        #  rhs should be a 2d mixture array of terminals and non terminals
        #  for example:
        #  left: S
        #  rhs: [[A,S,A], [B,S],[B,C]]
        self.rhs = rhs 

class terminal:
    def __init__(self,symbol):
        self.symbol = symbol
    
        

def unittest():
    pass