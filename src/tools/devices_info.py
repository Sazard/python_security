all_devices = []

class Device_info:
    def __init__(self, IP, alias, hostname):
        self.ip = IP
        self.port = []
        self.alias = alias
        self.hostname = hostname
    
    def AddDevice(IP, alias,hostname):
        all_devices.append(Device_info(IP, alias, hostname))

    def GetDevice(val):
        for d in all_devices:
            if d.alias == val or d.ip == val:
                return d

    def ToString(self):
        return "{\"name\" : \"" + self.name + "\", \"version\" : \"" + self.version + "\", \"license\" : \"" + self.liscence + "\", \"users\" : \"" + str(self.users) + "\"}"
