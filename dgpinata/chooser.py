import random
from pydantic import BaseModel

class Chooser(BaseModel):
    pass

class RandomObjectAttributeChooser(Chooser):
    """Pick a random object from a list and return the value of a specified attribute of that object."""

    object_eval_str: str # A string that can be evaluated to a list of objects
    attribute: str       # The attribute to return from the chosen object

    def invoke(
        self,
        sim,       # Even though this parameter is never used in the code, it might be used in the eval statement
        parent,    # Even though this parameter is never used in the code, it might be used in the eval statement
        timestamp, # Even though this parameter is never used in the code, it might be used in the eval statement
    ):
        obj_list = eval(self.object_eval_str)
        obj = random.choice(obj_list)
        attr = getattr(obj, self.attribute)
        return attr