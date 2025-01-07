class Password_state_machine:
    def __init__(self):
        # aditional variables to avoid typo errors
        self.lane = "Lane"
        self.triangle = "Triangle"
        self.cuadrilater = "Cuadrilater"
        self.pentagon = "Pentagon"
        self.circle = "circle"
        self.corners_to_tag = {
            3:self.triangle,
            4:self.cuadrilater,
            5:self.pentagon
        }
        self.initial_state = 0
        self.current_state = self.initial_state
        self.states = [1,2,3,0]
        self.alphabet = [self.lane,self.triangle, self.cuadrilater, self.pentagon, self.circle] 
        self.transitions = {
            0:[
                [self.alphabet ,0],
                [[self.circle, self.lane],1]
            ],
            1:[
                [self.alphabet ,0],
                [[self.cuadrilater],2]
            ],
            2:[
                [self.alphabet ,0],
                [[self.triangle, self.pentagon],3]
            ],
            3:[
                [self.alphabet ,0]
            ],
        }
    # function to go from one state to the next one based on caracter
    def evaluate(self, caracter): 
        if caracter in self.alphabet:
            for posible_state in self.transitions[self.current_state]:
                if caracter in posible_state[0]:
                    self.current_state = posible_state[1]
    
    def get_tag(self, n_corners):
        if n_corners in self.corners_to_tag:
            return self.corners_to_tag[n_corners]
        if n_corners > 5:
            return self.circle
        return self.lane
    