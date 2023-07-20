'''
Created on 2023. 7. 20.

@author: it
'''
import os
from pyboard.settings import STATIC_DIR, TEMPLATE_DIR
import pandas as pd
import folium
from folium import plugins
import urllib.request as req
from bs4 import BeautifulSoup as soup
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt


def makeChart(data):
    font_path = "c:/windows/fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)
    
    df = pd.DataFrame(data, columns=['title', 'point'])

    plt.xlabel('책제목')
    plt.ylabel('평점')
    plt.bar(range(len(df.title)), df.point, align="center")
    plt.xticks(range(len(df.title)), list(df.title), rotation=90)
    plt.savefig(os.path.join(STATIC_DIR, 'images/fig01.png'))

def web_craw(data):
    url = "https://www.yes24.com/product/Search?domain=All&query=python"
    res = req.urlopen(url) 
    bs = soup(res, 'html.parser')

    books = bs.select('#yesSchList > li')
    
    for book in books:
        title = book.select('div > div.item_info > div.info_row.info_name > a.gd_name')[0].get_text()
        author = book.select('div > div.item_info > div.info_row.info_pubGrp > span.authPub.info_auth')[0].get_text()
        price = book.select('div > div.item_info > div.info_row.info_price > strong > em')[0].get_text().replace(',', '')
        try:
            point = book.select('div > div.item_info > div.info_row.info_rating > span.rating_grade > em')[0].get_text()
        except: 
            point = 0.0
        data.append([title, author, price, point])

def cctv_map():
    popup = []
    locations = []
    path = os.path.join(STATIC_DIR, 'data/CCTV_20190917.csv')
    
    df = pd.read_csv(path)

    for data in df.values:
        if data[4] > 0 :
            popup.append(data[1])
            locations.append([data[10], data[11]])
    
    m = folium.Map(location=locations[0], zoom_start=11)
    plugins.MarkerCluster(locations, popup = popup).add_to(m)
    m.save(os.path.join(TEMPLATE_DIR, 'map/map01.html'))
    
    
