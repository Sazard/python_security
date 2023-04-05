class Device_info:
    def __init__(self,IP,port, alias):
        id = len(all_software)
        self.name = name
        self.version = version
        self.liscence = liscence
        self.users = users
    
    def GetAllSoftware():
        return all_software
    
    def AddSoftware(name,version,liscence,users):
        all_software.append(Software(name,version,liscence,users))

    def ToString(self):
        return "{\"name\" : \"" + self.name + "\", \"version\" : \"" + self.version + "\", \"license\" : \"" + self.liscence + "\", \"users\" : \"" + str(self.users) + "\"}"
