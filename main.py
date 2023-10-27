# WORK IN PROGRESS
# This is a script that generates a pdf report and a graph providing information about today's European energy prices
# as well as their evolution over time for the last 7 days

import datetime
from datetime import date

import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF


def average(prices):
    return sum(prices) / len(prices)


url = ''
average_arr = []
date_arr = []

pdf = FPDF()
pdf.add_page()

# pdf.add_font("Babel", "", "/home/andrei/.local/share/fonts/BabelStoneFlags.ttf")
# pdf.add_font("DejaVu", "", "/home/andrei/.local/share/fonts/DejaVuSans.ttf")
pdf.add_font("Noto", "", "/home/andrei/.local/share/fonts/NotoSans-Regular.ttf")

pdf.set_font("Noto", size=20)
pdf.cell(200, 10, "Daily report for energy prices in Europe", align='C')
# pdf.cell(200, 10, date.today().strftime('%Y-%m-%d'), align='C')
pdf.write(10, date.today().strftime('%d-%m-%Y'))

for day in range(0, 8):
    date = date.today() - datetime.timedelta(days=day)
    date_arr.append(date)
    # pdf.write(10, date.strftime('%Y-%m-%d'))
    url = 'https://euenergy.live/?date=' + date.strftime('%Y-%m-%d')
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    prices_table = soup.find('table', class_='prices_table')
    prices_arr = []
    if day == 0:
        pdf.set_font("Noto", size=9)
        pdf.write(10, "\n\nToday's energy prices (for the day-ahead segment)\n")
        # pdf.cell(40, 10, txt="Today's energy prices (for the day-ahead segment)", align='C', new_x=XPos.START, new_y=YPos.LAST)
    for country in prices_table.find_all('tbody'):
        rows = country.find_all('tr')
        for row in rows[1:]:
            if day == 0:
                pow_country = getattr(row.find('td'), 'text', None)
                pow_price = getattr(row.find('td', class_='price'), 'text', None)
                if "¹" in pow_country:
                    pow_country = pow_country.replace("¹", "")
                    pow_country = pow_country + " (zone 1)"
                elif "²" in pow_country:
                    pow_country = pow_country.replace("²", "")
                    pow_country = pow_country + " (zone 2)"
                elif "³" in pow_country:
                    pow_country = pow_country.replace("³", "")
                    pow_country = pow_country + " (zone 3)"
                elif "⁴" in pow_country:
                    pow_country = pow_country.replace("⁴", "")
                    pow_country = pow_country + " (zone 4)"
                pdf.write(10, pow_country + " " + pow_price + " Euro/MWh\n")
                # pdf.cell(200, 10, txt=pow_country + ' ' + pow_price + ' Euro/MWh', align='C')
                print(pow_country + " " + pow_price + " Euro/MWh")
            prices_arr.append(float(getattr(row.find('td', class_='price'), 'text', None)))

    average_arr.append(average(prices_arr))

for index, x in enumerate(average_arr):
    if index == 0:
        string = 'Average price of energy today (for the day-ahead segment) across all countries: %.2f Euro/MWh' % x
        print(string)
        pdf.set_font("Noto", size=11)
        # pdf.cell(200, 10, txt=string, align='C')
        pdf.write(10, string)
    else:
        print('Average price of energy ' + str(
            index) + ' days ago (for the day-ahead segment) across all countries: %.2f Euro/MWh' % x)

x = date_arr
y = average_arr

plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.xlabel('Date')
plt.ylabel('Price (Euro/MWh)')
plt.title('Evolution of energy price average (for the day-ahead segment) across all countries over the last 7 days')
# plt.show()
plt.savefig('graph.png')

pdf.image('graph.png')
pdf.output("Daily-Report.pdf")
