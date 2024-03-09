class VisionDescriptor:
    def __init__(self) -> None:
        self.__data_store:dict = dict()

    def add_element(self,name:str):
        self.__data_store[name] = dict()

    def add_element_attribute(self,name:str,attribute:str,value:str):
        assert (name in self.__data_store.keys()) ,"you have to add element, element didn't exit"
        assert (attribute not in self.__data_store.get(name)), "attribute alredy exit you have to use update function"
        self.__data_store.get(name)[attribute] = value
    def update_element_attribute(self,name:str,attribute:str,value:str):
        assert (name in self.__data_store.keys()) ,"you have to add element, element didn't exit"
        assert (attribute  in self.__data_store.get(name)), "attribute not exit you have to use add arrtibute function"
        self.__data_store.get(name)[attribute] = value
    
    
    def __len__(self,) ->int:
        return len(self.__data_store)
    def getVisionDes(self):
        # change 
        for key in self.__data_store.keys():
            objs = self.__data_store[key]
            out = """"""
            out += f"Object id: {key} below were there properties\n"
            for key_obj in objs.keys():
                out += f"\t{key_obj}: {objs[key_obj]}\n"
            yield out