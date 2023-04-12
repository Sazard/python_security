all_devices = []

class DeviceInfo:
    """
    A class to represent information about network devices.

    Attributes:
        ip (str): The IP address of the device.
        alias (str): An optional alias for the device.
        hostname (str): The hostname of the device.
        port (list): A list of open ports on the device.

    Methods:
        addDevice(ip, alias, hostname): Adds a new device to the list of known devices.
        getDevice(val): Returns the device with the given alias or IP address.
        __str__(): Returns a string representation of the device's information.
    """
    def __init__(self, ip, alias, hostname):
        """
        Initializes a new DeviceInfo object.

        Args:
            ip (str): The IP address of the device.
            alias (str, optional): An alias for the device. Defaults to None.
            hostname (str, optional): The hostname of the device. Defaults to None.
        """
        self.ip = ip
        self.ports = []
        self.alias = alias
        self.hostname = hostname
    
    def addDevice(ip, alias, hostname):
        """
        Adds a new device to the list of known devices.

        Args:
            ip (str): The IP address of the device.
            alias (str): An alias for the device.
            hostname (str): The hostname of the device.
        """
        all_devices.append(DeviceInfo(ip, alias, hostname))

    def getDevice(val):
        """
        Returns the device with the given alias or IP address.

        Args:
            val (str): The alias or IP address of the device to retrieve.

        Returns:
            DeviceInfo: The device with the given alias or IP address, or None if not found.
        """
        for d in all_devices:
            if d.alias == val or d.ip == val:
                return d
    
    def __str__(self):
        """
        Returns a string representation of the device's information. Works when we call 'print(device)'

        Returns:
            str: A string representation of the device's information.
        """
        return f"IP Address: {self.ip}\nAlias: {self.alias}\nHostname: {self.hostname}\nOpen Ports: {self.ports}\n"
