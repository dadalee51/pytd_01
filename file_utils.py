import pickle
import json
jd=json.dumps
jl=json.loads
class FileAction:
    filename='game_data'

    @staticmethod
    def write_to_file(obj):
        with open(FileAction.filename, "wb") as ofile:
            pickle.dump(obj,ofile)
    
    @staticmethod
    def read_from_file():
        with open(FileAction.filename, "rb") as infile:
            that_thing= pickle.load(infile)
            return that_thing
    
        