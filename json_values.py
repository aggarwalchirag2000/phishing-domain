import json

class Json_values:

    def __init__(self,file):
        self.file_name = file
    def data(self):

        try:
            with open(self.file_name,'r') as f:
                dic = json.load(f)
                f.close()

            keys,values,description = [],[],[]
            for items in dic['col_name'].keys():
                keys.append(items)
            for items in dic['col_name'].values():
                values.append(items)

            with open('cols_details.json','r') as f:
                dic = json.load(f)
                f.close()
            for items in dic.values():
                description.append(items)

            return keys,values,description

        except Exception as e:
            raise Exception