from socket import *
import datetime
from concurrent.futures import ThreadPoolExecutor
import threading
import ThreadSafeList

# Scan for open port
all_opened_port = None
number_of_thread = 32
current_ip = ""

def TestPort(port):
    global all_opened_port
    global current_ip
    s = socket(AF_INET, SOCK_STREAM)
    conn = s.connect_ex((current_ip, port))
    protocole = socket.getservbyport(port)
    if (conn == 0):
        all_opened_port.append(port)
        print(printServiceOnPort(port,  "tcp"))
        print("Port " + current_ip + ":" +  port + "  is Open with potocol :" + protocole)
    s.close()

def scan(devices):
    global all_opened_port
    global current_ip
    # devices = [(None,"192.168.1.152","192.168.1.152"),("test2","192.168.1.199","192.168.1.199"),("test3","192.168.1.245","192.168.1.254")]
    scan_result = {}
    for device in devices:
        hostname = device[0]
        alias = device[1]
        ip = device[2]

        device_info = [hostname, alias]
        print('Starting scan on host: ', ip)
        all_opened_port = ThreadSafeList.ThreadSafeList()
        current_ip = ip
        port_to_test = list(range(0,4096))
        with ThreadPoolExecutor(max_workers=number_of_thread) as executor:               
            executor.map(TestPort, port_to_test)
        
        executor.shutdown(wait=True, cancel_futures=False)
        print(all_opened_port)
        for i in all_opened_port.iterator():
            device_info.append(i)             
        scan_result[ip] = device_info
    return scan_result

# Create HTML report

def create_report(scan_result, output_format):
    now = datetime.datetime.now()
    report_file = 'network_scan_report_' + \
        now.strftime("%Y-%m-%d_%H-%M-%S") + '.' + output_format

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

            table {str(device_info[0])
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

    with open(report_file, 'w') as f:
        f.write(begin_doc_html)
        f.write('<p>Scan started at ' +
                now.strftime("%Y-%m-%d %H:%M:%S") + '</p>\n')
        f.write('<table>\n')
        f.write(
            '<tr><th>IP Address</th><th>Hostname</th><th>Alias</th><th>Open Ports</th></tr>\n')

        for ip, device_info in scan_result.items():

            ip = str(ip)
            hostname = str(device_info[0])
            alias = str(device_info[1])
            open_ports = str(device_info[2::])

            f.write('<tr><td>' + ip + '</td><td>' + hostname + '</td><td>' +
                    alias + '</td><td>' + open_ports + '</td></tr>\n')

        f.write('</table></body></html>')

    print('Scan complete. Report saved to ' + report_file)
