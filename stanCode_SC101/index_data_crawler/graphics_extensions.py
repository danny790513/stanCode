"""
graphics.py
Danny Tsai

This program will call the crawler to get index from
https://finance.yahoo.com/world-indices/
then draw the candlestick chart of each index.
"""
import index_data_crawler as crawler
import tkinter as tk
from tkinter import ttk

# Index name and index code
# INDICES = {
#     'TSEC weighted index': 'TWII',
#     'Dow Jones Industrial Average': 'DJI',
#     'S&P 500': 'GSPC',
#     'NASDAQ Composite': 'IXIC',
#     'Nikkei 225': 'N225',
#     'HANG SENG INDEX': 'HSI'}
INDICES = {
    'Dow Jones Industrial Average': 'DJI',
    'S&P 500': 'GSPC',
    'NASDAQ Composite': 'IXIC',
    'Nikkei 225': 'N225',
    'HANG SENG INDEX': 'HSI'}
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
GRAPH_MARGIN_SIZE = 20
TEXT_DX = 2
LINE_WIDTH = 2
CANDLESTICK_WIDTH = 4


def make_gui(top, width, height, indices, data):
    """
    Set up the GUI elements for candlestick chart.

    Input:
        top (Tkinter object): The main window..
        width (int): Width of canvas.
        height (int): Height of canvas.
        indices (dict): The data of index name and index code.
        data (dict): The data get from crawler.

    Returns:
        This function does not return any value.
    """
    label = tk.Label(top, text="Pick an index to show candlestick chart.", font=18)
    label.grid(row=0, column=0, sticky='w')
 
    index_picker = ttk.Combobox(top, values=list(indices.keys()), state="readonly", width=50)
    index_picker.grid(row=0, column=2, sticky='w')
    index_picker.current(0) 

    space = tk.LabelFrame(top, borderwidth=3, padx=2, pady=2)
    space.grid(row=1, columnspan=12, sticky='w') 
    canvas = tk.Canvas(space, width=width, height=height, name='canvas', bg='black')
    canvas.grid(row=3, columnspan=12, sticky='w')

    index_picker.bind(
        '<<ComboboxSelected>>', lambda event: draw_candlestick(canvas, data, indices, index_picker.get()))
    draw_candlestick(canvas, data, indices, index_picker.get())
    top.update()


def draw_candlestick(canvas, data, indices, index_name):
    """
    Draw candlestick on canvas by using given data

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        data (dict): The data get from crawler.
        indices (dict): The data of index name and index code.
        index_name (str): The index name want to draw.

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)
    index_code = indices[index_name] 
    d = data[index_code]
    highest = max(d[date]['high'] for date in d)
    lowest = min(d[date]['low'] for date in d)
    day = len(d)
    for key in d:
        x = get_x_coordinate(day, len(d))
        y_open = get_y_coordinate(highest, lowest, d[key]['open'])
        y_high = get_y_coordinate(highest, lowest, d[key]['high'])
        y_low = get_y_coordinate(highest, lowest, d[key]['low'])
        y_close = get_y_coordinate(highest, lowest, d[key]['close'])
        if day % 10 == 0:
            canvas.create_line(x, 0, x, CANVAS_HEIGHT, fill='grey', dash=(3, 5))
            canvas.create_text(
                x+TEXT_DX, CANVAS_HEIGHT, text=key, anchor=tk.SE, fill='white')

        if d[key]['open'] > d[key]['close']:
            canvas.create_line(x, y_high, x, y_low, fill='green') 
            canvas.create_rectangle(x-CANDLESTICK_WIDTH/2, y_open, x+CANDLESTICK_WIDTH/2, y_close, fill='green')
        elif d[key]['open'] < d[key]['close']:
            canvas.create_line(x, y_high, x, y_low, fill='red') 
            canvas.create_rectangle(x-CANDLESTICK_WIDTH/2, y_open, x+CANDLESTICK_WIDTH/2, y_close, fill='red')
        elif d[key]['open'] == d[key]['close']:
            canvas.create_line(x, y_high, x, y_low, fill='white') 
            canvas.create_rectangle(x-CANDLESTICK_WIDTH/2, y_open, x+CANDLESTICK_WIDTH/2, y_close, fill='white')
        day -= 1


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # delete all existing lines from the canvas
    canvas.create_line(
        GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE,
        CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, width=LINE_WIDTH, fill='white')
    canvas.create_line(
        GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE,
        CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, width=LINE_WIDTH, fill='white')


def get_x_coordinate(day, total_days):
    """
    Given the day and total_days to calculate x coordinate of the data on graphic.
    Input:
        day (int): Number of the day want to show on graphic.
        total_days (int): The total days in data.
    Returns:
        x_coordinate (int): The x coordinate.
    """
    x = (CANVAS_WIDTH - 2 * GRAPH_MARGIN_SIZE) / total_days * day + GRAPH_MARGIN_SIZE
    return x 


def get_y_coordinate(highest, lowest, price):
    """
    Given the prices to calculate y coordinate of the data on graphic.
    Input:
        highest (int): the highest price of all data.
        lowest (int): the lowest price of all data.
        price (int): the price of current data.
    Returns:
        y_coordinate (int): The y coordinate.
    """
    # x = (width - 2 * GRAPH_MARGIN_SIZE) / len(YEARS) * year_index + GRAPH_MARGIN_SIZE
    # return x   

    y = (CANVAS_HEIGHT - 2 * GRAPH_MARGIN_SIZE) * (highest-price)/(highest-lowest) + GRAPH_MARGIN_SIZE
    return y 


def main():
    """
    Get data from crawler and show graphic.
    """
    # Get data
    data = {}
    indices_code = list(INDICES.values())
    crawler.get_index_data(data, indices_code)
    # Make GUI
    top = tk.Tk()
    top.title('Index Data Crawler')
    make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, INDICES, data)
    top.mainloop()


if __name__ == '__main__':
    main()
