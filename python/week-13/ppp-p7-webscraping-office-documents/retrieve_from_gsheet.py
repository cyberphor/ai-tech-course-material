"""Module for using a web API"""
import pygsheets

def get_google_sheet():
    client = pygsheets.authorize(service_account_file="algebraic-ratio-338019-eb975aa8f686.json")
    workbook = client.open("Accounts") # name of Google Sheet
    return workbook.sheet1             # tab 1

def get_accounts_info(fields: list[str] = None, start: int = 0, end: int = 9):
    worksheet = get_google_sheet()
    accounts = []
    for record in worksheet.get_all_records()[start:(end+1)]:
        if None is fields:
            accounts.append(record)
        else:
            account = {}
            [account.update({field: record[field]}) for field in fields]
            accounts.append(account)
    return accounts
