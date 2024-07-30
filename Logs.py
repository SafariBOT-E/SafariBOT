import requests
import xml.etree.ElementTree as ET
from tkinter import Tk, Label, Button, Entry, Toplevel, ttk, StringVar
from tkcalendar import Calendar
from html2image import Html2Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# PRTG Dashboard API base URL
prtg_server = "https://safaritelecom.my-prtg.com"
prtg_user = "josephp@safari-solutions.com"
passhash = "3824428891"

def get_dates():
    def select_start_date():
        def on_date_select(e):
            global start_date
            start_date = cal.selection_get().strftime("%Y-%m-%d") + "-00-00-00"
            start_date_var.set(f"Start Date: {cal.selection_get().strftime('%Y-%m-%d')}")
            start_window.destroy()
        
        start_window = Toplevel(root)
        start_window.title("Select Start Date")

        style = ttk.Style(start_window)
        style.theme_use('clam')
        style.configure('Calendar', 
                        background='white', 
                        foreground='black', 
                        selectbackground='blue', 
                        selectforeground='white', 
                        weekendbackground='white', 
                        weekendforeground='black',
                        headersbackground='white', 
                        headersforeground='black', 
                        bordercolor='black')

        cal = Calendar(start_window, selectmode='day', style='Calendar')
        cal.pack(padx=10, pady=10)
        cal.bind("<<CalendarSelected>>", on_date_select)
    
    def select_end_date():
        def on_date_select(e):
            global end_date
            end_date = cal.selection_get().strftime("%Y-%m-%d") + "-23-59-59"
            end_date_var.set(f"End Date: {cal.selection_get().strftime('%Y-%m-%d')}")
            end_window.destroy()
        
        end_window = Toplevel(root)
        end_window.title("Select End Date")

        style = ttk.Style(end_window)
        style.theme_use('clam')
        style.configure('Calendar', 
                        background='white', 
                        foreground='black', 
                        selectbackground='blue', 
                        selectforeground='white', 
                        weekendbackground='white', 
                        weekendforeground='black',
                        headersbackground='white', 
                        headersforeground='black', 
                        bordercolor='black')

        cal = Calendar(end_window, selectmode='day', style='Calendar')
        cal.pack(padx=10, pady=10)
        cal.bind("<<CalendarSelected>>", on_date_select)

    def on_submit():
        global device_id
        device_id = device_id_entry.get()
        root.destroy()

    root = Tk()
    root.title("Enter Device ID and Dates")

    Label(root, text="Enter Device ID:").pack()
    device_id_entry = Entry(root)
    device_id_entry.pack(padx=10, pady=10)

    start_date_var = StringVar()
    end_date_var = StringVar()

    Button(root, text="Select Start Date", command=select_start_date).pack(pady=10)
    Label(root, textvariable=start_date_var).pack()

    Button(root, text="Select End Date", command=select_end_date).pack(pady=10)
    Label(root, textvariable=end_date_var).pack()

    Button(root, text="Submit", command=on_submit).pack(pady=10)

    root.mainloop()

get_dates()

# Construct the API URL
api_url = f"{prtg_server}/api/table.xml"
params = {
    "content": "messages",
    "columns": "objid,name,datetime,parent,status,sensor,device,group,probe,message,priority,type,tags,active",
    "count": "*",
    "id": device_id,
    "start": 1,
    "filter_dstart": start_date,
    "filter_dend": end_date,
    "username": prtg_user,
    "passhash": passhash,
}

# Make the API call
response = requests.get(api_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the XML response
    root = ET.fromstring(response.text)
    
    log_entries = []
    for item in root.findall(".//item"):
        status = item.find('status').text
        if status in ["Up", "Down"]:
            log_entry = {
                "ID": item.find('objid').text,
                "Datetime": item.find('datetime').text,
                "Device": item.find('device').text,
                "Status": item.find('status').text,
                "Message": item.find('message_raw').text,
            }
            log_entries.append(log_entry)
    
    # Create HTML table
    html_content = """
    <html>
    <head>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
                font-family: Arial, sans-serif;
            }
            th {
                background-color: #f2f2f2;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            h1 {
                font-family: "Times New Roman", serif;
                color: #2F5496;
            }
        </style>
    </head>
    <body>
        <h1>Network Logs Report</h1>
        <table>
            <tr>
                <th>ID</th>
                <th>Datetime</th>
                <th>Device</th>
                <th>Status</th>
                <th>Message</th>
            </tr>"""
    
    for entry in log_entries:
        html_content += f"""
            <tr>
                <td>{entry['ID']}</td>
                <td>{entry['Datetime']}</td>
                <td>{entry['Device']}</td>
                <td>{entry['Status']}</td>
                <td>{entry['Message']}</td>
            </tr>"""
    
    html_content += """
        </table>
    </body>
    </html>"""
    
    # Save HTML content to a file
    html_file = "network_logs_report.html"
    with open(html_file, "w") as file:
        file.write(html_content)
    
    print("HTML report generated successfully.")

    # Convert HTML to PNG using Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("file://" + os.path.abspath(html_file))
    time.sleep(2)  # Allow time for the page to fully render

    # Adjust window size to fit content
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
    driver.set_window_size(S('Width'), S('Height'))

    # Take screenshot
    driver.save_screenshot("network_logs_report.png")
    driver.quit()

    print("PNG report saved as 'network_logs_report.png'.")
else:
    print(f"Failed to retrieve logs: {response.status_code}")
