from random import randint

class Die:
    def __init__(self, dice=1, sides=20, mod=0):
        self.dice=dice
        self.sides=sides
        self.mod=mod
    
    def roll(self):
        result=self.mod
        for _ in range(self.dice):
            result+=randint(1, self.sides)
        return result
    
    def get_min(self):
        return self.dice+self.mod
    
    def get_max(self):
        return self.dice*self.sides+self.mod
    
    def get_average(self):
        return ((float(self.get_min())+float(self.get_max()))/2.0)

    def __str__(self):
        return f'{self.dice}d{self.sides}+{self.mod}'