import sys
sys.path.append("./")
from packages import *

class match_Describtion_values(BaseMatcher):

    def _matches(self, describtions):
        dsc1 = describtions[0]
        dsc2 = describtions[1]
        return sum(list(map(lambda d1, d2: abs(d1-d2)< 0.005, dsc1, dsc2)))
    def describe_to(self, description):
        description.append("Values are not close")

def is_good_Describtion_values():
    return match_Describtion_values()

def is_good_Describtion_keys(self):
    if not sum(list(map(lambda el : el in  ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'], self.val))):
        return self.error(f'Keys are not the same')
    return self
