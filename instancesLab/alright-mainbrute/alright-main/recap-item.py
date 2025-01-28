# If you DO have the WhatsApp Desktop app installed
from alright import WhatsApp
from time import sleep
from datetime import date,datetime,timedelta
import requests
import pandas
import json
import sys


#hournow = datetime.now().strftime("%H")
#if int(hournow) < 4:
#    startdate = (date.today() - timedelta(1)).strftime('%d/%m/%Y')
#    enddate = date.today().strftime("%d/%m/%Y")
#    starttime = "09:00"
#    endtime = "04:00"
#else:
#    startdate = date.today().strftime("%d/%m/%Y")
#    enddate = startdate
#    starttime = "09:00"
#    endtime = "23:59"
#
start = int(sys.argv[1])
end = int(sys.argv[2])
while start <= end:
    startdate = f"{start}/10/2023"
    if start == 31:
        enddate = f"1/11/2023"
    else:
        enddate = f"{start+1}/10/2023"
    starttime = "07:00"
    endtime = "07:00"

    print(startdate, enddate, starttime, endtime)
    start = start + 1

    MINUMAN = 0
    MAKANAN = 0
    BEER = 0
    OPEN_BILL = 0
    PAKET_PROMO = 0 
    PARKIR = 0



    #GET SALES BY ITEM
    laporan_sales_by_item_cookies = {
        'csrf_cookie_mpos': '5b0c7b868ca031f555e490e9b29fd8de',
        'cookiesession1': '582E227AX2XLTOJCDDGAQX84O1CA8C39',
        'ci_session': 'a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%226cc9f323d838b0fb08b877caa0d437da%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2210.100.100.62%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1681220365%3B%7D9de35c481dcfcac35d873096c53557970a219bda',
    }
    
    laporan_sales_by_item_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en,en-US;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarysiBE1ArGJV7KadH1',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'csrf_cookie_mpos=5b0c7b868ca031f555e490e9b29fd8de; cookiesession1=582E227AX2XLTOJCDDGAQX84O1CA8C39; ci_session=a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%226cc9f323d838b0fb08b877caa0d437da%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2210.100.100.62%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1681220365%3B%7D9de35c481dcfcac35d873096c53557970a219bda',
        'Origin': 'https://backoffice.dretail.id',
        'Referer': 'https://backoffice.dretail.id/admin/c_report_mt_salesbyitem',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    
    laporan_sales_by_item_data = '------WebKitFormBoundarysiBE1ArGJV7KadH1\r\nContent-Disposition: form-data; name="csrf_token_mpos"\r\n\r\n5b0c7b868ca031f555e490e9b29fd8de\r\n------WebKitFormBoundarysiBE1ArGJV7KadH1\r\nContent-Disposition: form-data; name="radio-duration"\r\n\r\nall-day\r\n------WebKitFormBoundarysiBE1ArGJV7KadH1\r\nContent-Disposition: form-data; name="time-left"\r\n\r\n00\r\n------WebKitFormBoundarysiBE1ArGJV7KadH1\r\nContent-Disposition: form-data; name="time-left"\r\n\r\n00\r\n------WebKitFormBoundarysiBE1ArGJV7KadH1\r\nContent-Disposition: form-data; name="time-right"\r\n\r\n00\r\n------WebKitFormBoundarysiBE1ArGJV7KadH1\r\nContent-Disposition: form-data; name="time-right"\r\n\r\n00\r\n------WebKitFormBoundarysiBE1ArGJV7KadH1\r\nContent-Disposition: form-data; name="branch"\r\n\r\n0\r\n------WebKitFormBoundarysiBE1ArGJV7KadH1\r\nContent-Disposition: form-data; name="arr_branch"\r\n\r\n0\r\n------WebKitFormBoundarysiBE1ArGJV7KadH1\r\nContent-Disposition: form-data; name="arr_staff"\r\n\r\n\r\n------WebKitFormBoundarysiBE1ArGJV7KadH1\r\nContent-Disposition: form-data; name="reportrange"\r\n\r\n%s - %s\r\n------WebKitFormBoundarysiBE1ArGJV7KadH1\r\nContent-Disposition: form-data; name="duration"\r\n\r\n%s - %s\r\n------WebKitFormBoundarysiBE1ArGJV7KadH1\r\nContent-Disposition: form-data; name="flagEachday"\r\n\r\nfalse\r\n------WebKitFormBoundarysiBE1ArGJV7KadH1\r\nContent-Disposition: form-data; name="column"\r\n\r\n[{"name":"column[]","value":"item_name"},{"name":"column[]","value":"modifier"},{"name":"column[]","value":"category_name"},{"name":"column[]","value":"qty"},{"name":"column[]","value":"grosssales"},{"name":"column[]","value":"void"},{"name":"column[]","value":"voidamount"},{"name":"column[]","value":"discount"},{"name":"column[]","value":"discount_bill"},{"name":"column[]","value":"total"},{"name":"column[]","value":"service"},{"name":"column[]","value":"tax"},{"name":"column[]","value":"grandtotal"}]\r\n------WebKitFormBoundarysiBE1ArGJV7KadH1\r\nContent-Disposition: form-data; name="companyid"\r\n\r\n8733\r\n------WebKitFormBoundarysiBE1ArGJV7KadH1\r\nContent-Disposition: form-data; name="company_type"\r\n\r\n0\r\n------WebKitFormBoundarysiBE1ArGJV7KadH1--\r\n' % (startdate, enddate, starttime, endtime)
    
    response = requests.post('https://backoffice.dretail.id/mpos-server/index.php/C_report_mt_salesitem/exportXls', cookies=laporan_sales_by_item_cookies, headers=laporan_sales_by_item_headers, data=laporan_sales_by_item_data)
    
    open('laporan_sales_by_item.xlsx', 'wb').write(response.content)
    excel = pandas.read_excel('laporan_sales_by_item.xlsx',skiprows=7)
    data = excel.to_json()
    json_data = json.loads(data)
    
    
    ### GET OPEN BILL ###
    cookies = {
        'csrf_cookie_mpos': '5b0c7b868ca031f555e490e9b29fd8de',
        'cookiesession1': '582E227AX2XLTOJCDDGAQX84O1CA8C39',
        'ci_session': 'a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22e1f12245cd75ec9cb853eb10efe2cc47%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2210.100.100.62%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1681234190%3B%7Dd6f22faf3f2fdf22bcb4c85ccbe5e18db99b45b5',
    }
    
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en,en-US;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'csrf_cookie_mpos=5b0c7b868ca031f555e490e9b29fd8de; cookiesession1=582E227AX2XLTOJCDDGAQX84O1CA8C39; ci_session=a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%22e1f12245cd75ec9cb853eb10efe2cc47%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2210.100.100.62%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1681234190%3B%7Dd6f22faf3f2fdf22bcb4c85ccbe5e18db99b45b5',
        'Origin': 'https://backoffice.dretail.id',
        'Referer': 'https://backoffice.dretail.id/admin/c_report_salesrealtime',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    
    data = {
        'draw': '1',
        'branch': '10210',
        'status': 'all status',
        'date': 'today',
        'columns[0][name]': '',
        'order[0][column]': '0',
        'order[0][dir]': '',
    }
    
    response = requests.post('https://backoffice.dretail.id/mpos-server/index.php/C_report_salesrealtime/getData', cookies=cookies, headers=headers, data=data)
    
    data = response.content
    reff_json_data = json.loads(data)
    
    
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en,en-US;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'csrf_cookie_mpos=5b0c7b868ca031f555e490e9b29fd8de; cookiesession1=582E227AX2XLTOJCDDGAQX84O1CA8C39; ci_session=a%3A4%3A%7Bs%3A10%3A%22session_id%22%3Bs%3A32%3A%220cb2a0943ed7a03715ed2f69c4c33e9d%22%3Bs%3A10%3A%22ip_address%22%3Bs%3A13%3A%2210.100.100.62%22%3Bs%3A10%3A%22user_agent%22%3Bs%3A111%3A%22Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Safari%2F537.36%22%3Bs%3A13%3A%22last_activity%22%3Bi%3A1681232034%3B%7D34e2a6c0802f02b1e3a1662b569ede76e0af1bb1',
        'Origin': 'https://backoffice.dretail.id',
        'Referer': 'https://backoffice.dretail.id/admin/c_report_salesrealtime',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    for v in reff_json_data["data"]:
        if v["reff_number"] != "":
            reff_num = v["reff_number"]
            data = {
                'reffnumber': reff_num,
                'csrf_token_mpos': '5b0c7b868ca031f555e490e9b29fd8de',
            }
    
            response = requests.post(
                'https://backoffice.dretail.id/mpos-server/index.php/C_report_salesrealtime/details',
                cookies=cookies,
                headers=headers,
                data=data,
            )
    
            data = response.content
            opbill_data = json.loads(data)
            qty = opbill_data["txnproductitem"]["bill"]["qty"]
            OPEN_BILL = OPEN_BILL + qty
    
    
    for (item_name), (category), (item_sold), (item_void) in zip(json_data["Item Name"].values(),json_data["Category"].values(),json_data["Item Sold"].values(),json_data["Item Void"].values()):
        if (category == "ESPRESSO BASED" or category == "TEA" or category == "MANUAL BREW" or category == "MOCKTAIL" or category == "POWDER BASED"):
           MINUMAN = MINUMAN + item_sold - item_void 
        elif category == "EATS AND BITES":
           MAKANAN = MAKANAN + item_sold - item_void 
        elif category == "BEER":
           BEER = BEER + item_sold - item_void 
        elif category == "Parkir":
           PARKIR = PARKIR + item_sold - item_void 
        elif "Paket" in str(category):
           if "Jomblo" in str(item_name):
                PAKET_PROMO = PAKET_PROMO + (item_sold*1) - (item_void*1)
           if "Romantis" in str(item_name):
                PAKET_PROMO = PAKET_PROMO + (item_sold*3) - (item_void*3)
           if "Ngeghibah" in str(item_name):
                PAKET_PROMO = PAKET_PROMO + (item_sold*6) - (item_void*6)
    MINUMAN = MINUMAN + BEER 
    MAKANAN = MAKANAN + PAKET_PROMO
    
    
    msg = f"*ITEM*\nMINUMAN: {MINUMAN}\nMAKANAN: {MAKANAN}\nPARKIR: {PARKIR}\n"
    print(msg)
    
