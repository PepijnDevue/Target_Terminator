import json
import numpy as np
from typing import Any


class NumpyEncoder(json.JSONEncoder):
    """
    NummpyEncoder class.

    This class overrides the default method of the json.JSONEncoder,
    such that it can convert numpy arrays to lists on the fly.

    See json.JSONEncoder for more information.

    @public methods:
    + default(obj: Any)-> Any
        For each object in the to-parse json file, this function will
        convert it to a list if it is a numpy array or bool.
    """
    def default(self, obj: Any)-> Any:
        """
        Default converter for json files.

        Converts numpy arrays to lists and numpy bools to bools,
        ignores any others.

        @params:
            - obj (Any): Object to encode.
        
        @returns:
            - Any, with exclusion of numpy arrays, as these are 
            converted to lists and numpy bools, which are cast to bools.
        """
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        return super().default(obj)
