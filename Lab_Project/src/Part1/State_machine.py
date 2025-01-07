class Password_state_machine:
    def __init__(self):
        self.initial_state = 0
        self.current_state = self.initial_state
        self.states = [1,2,3,0]
        self.alphabet = [True,False] 
        self.transitions = {
            0:[
                [[True,False] ,0],
                [[True],1]
            ],
            1:[
                [[True,False] ,0],
                [[True],2]
            ],
            2:[
                [[True,False] ,0],
                [[True],3]
            ],
            3:[
                [[True,False] ,0]
            ],
        }
    # function to go from one state to the next one based on caracter
    def evaluate(self, caracter): 
        if caracter in self.alphabet:
            for posible_state in self.transitions[self.current_state]:
                if caracter in posible_state[0]:
                    self.current_state = posible_state[1]
    