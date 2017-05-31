import os
from bs4 import BeautifulSoup as Soup

from config import TEMPLATES_DIR
from bokeh.charts import TimeSeries
# from bokeh.resources import CDN
from bokeh.embed import components



def get_plot_ticker_components(ticker, df_data):
    plot_title = 'Last Month ' + ticker.upper() + ' Closing Price'

    p = TimeSeries(df_data, legend=True, title=plot_title, xlabel='Date', ylabel='Stock Prices')
    p.title.text_font_size = '14pt'

    script, div = components(p)

    return script, div


def add_script_to_html(script, soup):
    # convert script to bs
    soup_script = Soup(script, 'html.parser')
    # get contents
    script_content = soup_script.find('script').contents[0]

    # find location in template and create script tag
    first_script = soup.find('script')

    script_plot = soup.new_tag('script', type='text/javascript')
    #script_plot = soup.new_tag('script')
    script_plot.string = script_content
    # add script to template
    first_script.insert_after(script_plot)

    return soup


def add_div_to_html(div, soup):
    outer_div_class = Soup(div).find_all('div')[0].get('class')
    inner_div_class = Soup(div).find_all('div')[1].get('class')
    inner_div_id = Soup(div).find_all('div')[1].get('id')

    # create new tags
    outer_div_tag = soup.new_tag('div', **{'class': outer_div_class})
    inner_div_tag = soup.new_tag('div', **{'class': inner_div_class, 'id': inner_div_id})

    # add tags
    body_tag = soup.find('body')
    body_tag.insert(-1, outer_div_tag)

    # get_div_tag1 = soup.find_all('div')
    # get_div_tag1[1].insert(0, outer_div_tag)

    get_div_tags = soup.find_all('div')
    get_div_tags[1].insert(0, inner_div_tag)

    return soup


def convert_plot_html(script, div, html_template_text=html):
    soup = Soup(html_template_text, 'html.parser')
    soup = add_script_to_html(script, soup)
    soup = add_div_to_html(div, soup)

    with open(os.path.join(TEMPLATES_DIR, 'closing_price_plot.html'), 'w') as f:
        f.write(str(soup))
