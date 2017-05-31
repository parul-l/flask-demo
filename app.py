from flask import Flask, render_template, request, redirect
import get_data as gd
import plot_stock_prices as psp

# import os
# from bs4 import BeautifulSoup as Soup
# 
# from config import TEMPLATES_DIR

app = Flask(__name__)


@app.route('/')
def main():
    return redirect('/index')

### BASIC WAY ########
# @app.route('/index', methods=['GET', 'POST'])
# def index():
#     if request.method == 'GET':
#         return render_template('index.html')
# 
#     else:
#         ticker_input = request.form['ticker_symbol']
#         df_data = gd.get_data_df(ticker=ticker_input)
#         try:
#             psp.plot_ticker(ticker=ticker_input, df_data=df_data)
#             return redirect('/plot')
#         except:
#             return redirect('/error_page')
# 
# 
# @app.route('/plot', methods=['GET'])
# def plot_stock():
#     return render_template('closing_price_plot.html')
# 
# 
# @app.route('/error_page', methods=['GET'])
# def error_page():
#     return render_template('error_page.html')


###### SCRIPT/DIV WAY ######
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    else:
        ticker_input = request.form['ticker_symbol']
        df_data = gd.get_data_df(ticker=ticker_input)
        if len(df_data) > 0:
            script, div = psp.get_plot_ticker_components(
                ticker=ticker_input,
                df_data=df_data
            )
            psp.convert_plot_html(
                script=script,
                div=div,
                html_template_text=psp.html
            )
            return redirect('/plot')
        else:
            return redirect('/error_page')


@app.route('/plot', methods=['GET', 'POST'])
def plot_stock():
    return render_template('closing_price_plot.html')


@app.route('/error_page', methods=['GET', 'POST'])
def error_page():
    return render_template('error_page.html')


if __name__ == '__main__':
    # app.run(port=33507)
    app.run(host='0.0.0.0')
