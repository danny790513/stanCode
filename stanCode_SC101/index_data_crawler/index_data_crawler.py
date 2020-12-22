"""
index_data_crawler.py
Danny Tsai

This program will get index from
https://finance.yahoo.com/world-indices/
of indices and put in dictionary given.
"""
import requests
from bs4 import BeautifulSoup


def main():
	"""
	This program will get index from
	https://finance.yahoo.com/world-indices/
	of indices and put in dictionary given.
	"""
	d = {}
	indices = ['TWII', 'DJI', 'GSPC', 'IXIC', 'N225', 'HSI']
	get_index_data(d, indices)
	print_data(d, indices[-1])
	for index in indices:
		print_data(d, index)


def get_index_data(d, indices_code):
	"""
	This function will get html from website,
	and call interpret_html function
	Input:
		d (dict): a empty dictionary.
		indices_code(list): code of indices want to get data from website
	Returns:
		This function does not return any value.
	"""
	for index in indices_code:
		d[index] = {}
		url = f'https://finance.yahoo.com/quote/%5E{index}/history?p=%5E{index}'
		response = requests.get(url)
		html = response.text
		interpret_html(d, index, html)


def interpret_html(d, index_code, html):
	"""
	This function will get html from website,
	and call interpret_html function
	Input:
		d (dict): dictionary given from get_index_data function.
		index_code(str): code of index from indices_code.
		html(str): html text from website.

	Returns:
		This function does not return any value.
	"""
	column_label = ['open', 'high', 'low', 'close', 'adj close', 'volumn']
	soup = BeautifulSoup(html, 'html.parser')
	tr = soup.find_all('tr', {'class': 'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)'})
	for r in tr:
		td = r.find_all('td')
		date = td[0].text
		d[index_code][date] = {}
		for i in range(len(column_label)):
			if td[i+1].text == '-':
				d[index_code][date][column_label[i]] = None
			else:	
				d[index_code][date][column_label[i]] = float(td[i+1].text.replace(',', ''))


def print_data(d, index_code):
	"""
	Call this function for print dictionary.
	Input:
		d (dict): dictionary.
		index_code(str): code of index from indices_code.

	Returns:
		This function does not return any value.
	"""
	for date, price in d[index_code].items():
		print(f"{date}, close:{price['close']}")


if __name__ == '__main__':
	main()
