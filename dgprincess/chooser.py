import random
from pydantic import BaseModel

class Chooser(BaseModel):
    pass

class RandomObjectAttributeChooser(Chooser):
    object_eval_str: str
    attribute: str

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