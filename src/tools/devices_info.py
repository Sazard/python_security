import json

all_devices = []

class DeviceInfo:
    """
    A class to represent information about network devices.

    :ivar ip: The IP address of the device.
    :vartype ip: str
    :ivar alias: An optional alias for the device.
    :vartype alias: str
    :ivar hostname: The hostname of the device.
    :vartype hostname: str
    :ivar port: A list of open ports on the device.
    :vartype port: list
    """
    def __init__(self, ip, alias, hostname):
        """
        Initializes a new DeviceInfo object.

        :param ip: The IP address of the device.
        :type ip: str
        :param alias: An alias for the device. Defaults to None.
        :type alias: str, optional
        :param hostname: The hostname of the device. Defaults to None.
        :type hostname: str, optional
        """
        self.ip = ip
        self.ports = []
        self.alias = alias
        self.hostname = hostname
    
    def addDevice(ip, alias, hostname):
        """
        Adds a new device to the list of known devices.

        :param ip: The IP address of the device.
        :type ip: str
        :param alias: An alias for the device.
        :type alias: str
        :param hostname: The hostname of the device.
        :type hostname: str
        """
        all_devices.append(DeviceInfo(ip, alias, hostname))

    def getDevice(val):
        """
        Returns the device with the given alias or IP address.

        :param val: The alias or IP address of the device to retrieve.
        :type val: str
        :return: The device with the given alias or IP address, or None if not found.
        :rtype: DeviceInfo
        """
        for d in all_devices:
            if d.alias == val or d.ip == val:
                return d

    def matchPorts(self):
        """
        Returns a string containing open ports along with the matching service usually opened on that port

        :return: A string containing open ports usage information
        :rtype: str
        """
        ret = "["
        
        with open('tools/common_ports.json') as f:
            data = json.load(f)

            for p in self.ports:
                ret += str(p)
                
                if p <= 1000:
                    port_name = data[str(p)]['name']
                    if port_name != "":
                        ret += " (" + port_name + ")"
                ret += ", "

        return ret[:-2] + "]"
            
    
    def __str__(self):
        """
        Returns a string representation of the device's information. Works when we call 'print(device)'.

        :return: A string representation of the device's information.
        :rtype: str
        """
        ports = self.matchPorts()

        return f"IP Address: {self.ip}\nAlias: {self.alias}\nHostname: {self.hostname}\nOpen Ports: {ports}\n"
