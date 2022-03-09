import pandas as pd
import os

import json

class Validation:
    def __init__(self,file,location,jsonn):
        self.file = file
        self.name = location
        self.location = "./"+location+"/" + str(file.filename)
        self.jsonn = jsonn


    def save(self):
        try:
            self.file.save(os.path.join(self.name,self.file.filename))
        except Exception:
            raise Exception


    def checkFile(self):
        try:
            data = pd.read_csv(self.location)
            with open(self.jsonn,'r') as f:
                dic = json.load(f)
                f.close()
            numberofcols = dic['NumberofColumns']
            if(data.shape[1] != numberofcols):
                os.remove(self.location)
                raise ValueError("abcd")
            col_name = dic['col_name']
            return numberofcols,col_name

        except UnicodeDecodeError:
            os.remove(self.location)
            raise UnicodeDecodeError

        except ValueError:
            raise ValueError

        except Exception:
                raise Exception


