from socket import *
import datetime
from concurrent.futures import ThreadPoolExecutor
import threading
from tools import ThreadSafeList
from tools import devices_info
import json
import csv

# Scan for open port
all_open_ports = None
number_of_thread = 32
current_ip = ""

def test_port(port):
    """
    Tests if a port is open or closed for a given IP address.

    This function is called by each thread to ping all ports in the port_to_test list.

    :param port: The port to test.
    :type port: int
    """
    #recover global variable  between thread
    global all_open_ports
    global current_ip
    #socket creation
    s = socket(AF_INET, SOCK_STREAM)
    #ping
    conn = s.connect_ex((current_ip, port))
    if (conn == 0):
        all_open_ports.append(port)
        print("Port " + current_ip + ":" +  port + "  is Open")
    s.close()

def scan():
    """
    Scans all IP addresses in the network for open ports.

    :return: A dictionary containing the scan results. The keys are the IP addresses, and the values are lists of open ports.
    :rtype: dict
    """
    global all_open_ports
    global current_ip
    # devices = [(None,"192.168.1.152","192.168.1.152"),("test2","192.168.1.199","192.168.1.199"),("test3","192.168.1.245","192.168.1.254")]
    scan_result = {}
    for device in devices_info.all_devices:
        hostname = device.hostname
        alias = device.alias
        ip = device.ip


        print('Starting scan on host: ', ip)
        #reset oppened port between ip
        all_open_ports = ThreadSafeList.ThreadSafeList()
        current_ip = ip

        #create a list of port to create
        port_to_test = list(range(0,4096))
        
        #threadpool to ping all port in the port_to_test list
        with ThreadPoolExecutor(max_workers=number_of_thread) as executor:               
            executor.map(test_port, port_to_test)
        
        #wait for all thread to finish
        executor.shutdown(wait=True, cancel_futures=False)
         
        devices_info.DeviceInfo.getDevice(ip).ports = all_open_ports.iterator()
    return scan_result

# Create HTML report
def create_report(output_format):
    """
    Generates a report of the scan results in the specified format.

    :param output_format: The format of the report. Can be "html", "csv", or "json".
    :type output_format: str
    :return: None
    """
    # get the current date and time
    now = datetime.datetime.now()

    # create a filename for the report
    report_file = 'network_scan_report_' + \
        now.strftime("%Y-%m-%d_%H-%M-%S") + '.' + output_format

    # create the beginning of the HTML report
    if output_format == "html":
        begin_doc_html = """
        <html>
        <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                margin-left: 20px;
            }
            table {
                border-collapse: collapse;
                margin: 20px 0;
            }
            th,
            td {
                border: 1px solid #333;
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #eee;
            }
        </style>
        </head>
        <body>
        <h1>Network Scan Report</h1>
        """

    # create the report file and write the scan results to it
    with open(report_file, 'w', newline='') as f:
        if output_format == "csv":
            writer = csv.writer(f)
            writer.writerow(['IP Address', 'Hostname', 'Alias', 'Open Ports'])
            for device in devices_info.all_devices:
                ip = str(device.ip)
                hostname = str(device.hostname)
                alias = str(device.alias)
                open_ports = str(device.ports)
                writer.writerow([ip, hostname, alias, open_ports])

        elif output_format == "json":
            data = []
            for device in devices_info.all_devices:
                ip = str(device.ip)
                hostname = str(device.hostname)
                alias = str(device.alias)
                open_ports = str(device.ports)
                data.append({'IP Address': ip, 'Hostname': hostname, 'Alias': alias, 'Open Ports': open_ports})

            json.dump(data, f)

        elif output_format == "html":
            f.write(begin_doc_html)
            f.write('<p>Scan started at ' +
                    now.strftime("%Y-%m-%d %H:%M:%S") + '</p>\n')
            f.write('<table>\n')
            f.write(
                '<tr><th>IP Address</th><th>Hostname</th><th>Alias</th><th>Open Ports</th></tr>\n')

            for device in devices_info.all_devices:

                ip = str(device.ip)
                hostname = str(device.hostname)
                alias = str(device.alias)
                open_ports = str(device.ports)

                f.write('<tr><td>' + ip + '</td><td>' + hostname + '</td><td>' +
                        alias + '</td><td>' + open_ports + '</td></tr>\n')

            f.write('</table></body></html>')

    # print a message indicating the report was created
    print('Scan complete. Report saved to ' + report_file)
