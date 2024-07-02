"""
This file is get information about crypto
Create by: Sergey Tovmasyan
Date: 12.06.2024
"""
import os
import tkinter
from tkinter import filedialog
import xlsxwriter
import requests
def open_file():
    get_name = []
    def fff():
        """
        Function: open_file
        Brief: you choose file and get names of crypto
        Params:None
        Return:None
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path,encoding = 'utf - 8') as file:
                content = file.readlines()
                for i in content:
                    get_name.append(i.strip())
        else:
            get_name.append("Bitcoin")
        root.destroy()
    root = tkinter.Tk()
    root.title("File Opener")
    root.geometry("300x250+200+200")
    open_button = tkinter.Button(root, text="find File", command=fff)
    open_button.pack()
    root.mainloop()
    return get_name
def get_crypto_data():
    """
    Function: get_crypto_data
    Brief: The function request url and get all data about crypto
    Params:
    Return: returns the list of crypto data
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd","price_change_percentage":"24h"}
    try:
        response = requests.get(url, params=params,timeout = 10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error {e}")
        return []
def get_data_by_name(cnt,content):
    """
    Function: get_data_by_name
    Brief: The functions is search crypto by name and get info about crypto
    Params: cnt`name of crpto,content`data of crypto
    Return: return list of crypto by name
    """
    data = []
    for line in cnt:
        for i in range(len(cnt)):
            if line.lower() == content[i]['name'].lower():
                data.append({
                'name': content[i]['name'],
                'symbol': content[i]['symbol'],
                'current_price': content[i]['current_price'],
                'market_cap': content[i]['market_cap'],
                'total_volume': content[i]['total_volume'],
                'price_change_24h': content[i]['price_change_24h']
            })
    return data
def write_in_xlsx(cnt):
    """
    Function: write_in_xlsx
    Brief: The functions is open window user input xlsx name and all data by name input in xlsx file
    Params: cnt`data of crptto by name
    Return: none
    """
    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")
    if not file_path:
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        file_path = os.path.join(downloads_folder, "default_filename.xlsx")
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet("Sheet")
    bold_green_format = workbook.add_format({'bg_color' : 'green','bold': True})
    top_name = []
    for i in cnt[0]:
        top_name.append(i)
    row,col = 0,0
    for i in top_name:
        worksheet.write(row,col,i,bold_green_format)
        col += 1
    row = 1
    for crypto in cnt:
        col = 0
        for i in crypto.values():
            worksheet.write(row,col,i)
            col += 1
        row += 1
    for col_num, header in enumerate(top_name):
        column_len = max(len(header), max(len(str(row[header])) for row in cnt)) + 2
        worksheet.set_column(col_num, col_num, column_len)
    workbook.close()
def main():
    get_name = open_file()
    data = get_crypto_data()
    if data == []:
        print("error in request")
        exit()
    data_by_name = get_data_by_name(get_name,data)
    if data_by_name == []:
        print("error in crypto name")
        exit()
    write_in_xlsx(data_by_name)
if __name__ == "__main__":
    main()
