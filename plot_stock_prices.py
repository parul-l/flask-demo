from bokeh.charts import TimeSeries
from bokeh.embed import components


def get_plot_ticker_components(ticker, df_data):
    plot_title = 'Last Month ' + ticker.upper() + ' Closing Price'

    p = TimeSeries(df_data.closing_price, legend=True, title=plot_title, xlabel='Date', ylabel='Stock Prices')
    p.title.text_font_size = '14pt'

    script, div = components(p)

    return script, div
