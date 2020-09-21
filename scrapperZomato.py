#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd                  #For data eploration.
from bs4 import BeautifulSoup        #For scraping the website.
import requests                      #For sending the requests to the website.
from nltk import word_tokenize       #For cleaning the text data.
import json                          #For reading json data
from tqdm.notebook import tqdm       #For checking the loop timinngs.
import seaborn as sns                #For visualization.
from matplotlib import pyplot as plt #For visualization.
# import folium                        #For Map Visualization
import re                            #Regular Expression
import operator


# In[ ]:


headers = {'User-Agent': 'Mozilla/5.0'}
name_=[]  #For saving Restaurant's name
online_=[] #For saving Restaurant's 
title_=[]  #For saving Restaurant's type
area_=[]   #For saving Restaurant's area
rating_=[] #For saving Restaurant's rating
votes_=[]  #For saving Restaurant's votes
add_=[]    #For saving Restaurant's address
cuisines_=[]#For saving Restaurant's cuisines
cf2_=[]    #For saving Restaurant's cost for 2 persons
hours_=[]  #For saving Restaurant's timings
link_=[]   #For saving Restaurant's web link
json_=[]   #For saving Restaurant's json file
dish_=[]   #For saving Restaurant's dish   
price_=[]  #For saving Restaurant'sdish price
contact_=[] #For saving Restaurant's Contact number
url='https://www.swiggy.com/sultanpur?page='
for page in tqdm(range(1,9)):
    print(f'{url}{page}')
    r=requests.get(f'{url}{page}',headers=headers)
    print(r)
    soup=BeautifulSoup(r.text,'html.parser')
    cards=soup.find_all(class_='card search-snippet-card search-card')
    for card in cards:
        try:
            contact=card.find(class_='item res-snippet-ph-info')['data-phone-no-str']
            contact_.append(contact)
        except:
            contact_.append(0)
        try:
          content=card.find(class_='content')
          online=card.find('span',class_='fontsize4 bold action_btn_icon o2_closed_now')
          if online:
            online_.append('Delivery Available')
          else:
            online_.append('Delivery Not Available')
        except:
          online_.append('Delivery Not Available')
        try:
            title=content.find(class_='res-snippet-small-establishment mt5').find('a').getText()
            title_.append(title)
        except:
            title_.append(0)
        try:
            name=content.find('a',class_='result-title hover_feedback zred bold ln24 fontsize0').getText()
            name_.append(name)
        except:
            name_.append(0)
        try:
            area=content.find(class_='row').find(class_='row').find('a').find_next('a').find_next('a').getText()
            area_.append(area)
        except:
            area_.append(0)
        try:
            rating=content.find(class_='row').find(class_='row').find(class_='ta-right floating search_result_rating col-s-4 clearfix').find('div').getText()
            rating_.append(rating)
        except:
            rating_.append(0)
        try:
            votes=content.find(class_='row').find(class_='row').find(class_='ta-right floating search_result_rating col-s-4 clearfix').find('span').getText()
            votes_.append(votes)
        except:
            votes_.append(0)
        try:
            add=content.find(class_='row').find(class_='row').find_next(class_='row').find('div').getText()
            add_.append(add)
        except:
            add_.append(0)
        try:    
            cuisines=content.find(class_='search-page-text clearfix row').find(class_='clearfix').find('span').find_next('span').getText()
            cuisines_.append(cuisines)
        except:
            cuisines_.appned(0)
        try:
            cf2=content.find(class_='search-page-text clearfix row').find(class_='res-cost clearfix').find('span').find_next('span').getText()
            cf2_.append(cf2)
        except:
            cf2_.append(0)
        try:    
            hours=content.find(class_='search-page-text clearfix row').find(class_='res-timing clearfix')('div')[0].getText()
            hours_.append(hours)
        except:
            hours_.append(0)
        try:
            link=content.find('a',class_='result-title hover_feedback zred bold ln24 fontsize0')['href']
            link_.append(link)
        except:
            link_.appned(0)
        r=requests.get(f'{link}/order',headers=headers)
        soup=BeautifulSoup(r.text,'html.parser')
        try:
            _json=soup.find('script',type='application/ld+json').find_next('script',type='application/ld+json')
            _json=_json.getText()
            _json=json.loads(_json)
            json_.append(_json)
        except:
            json_.append(0)
        if online:
            try:
                    
                dish=soup.find(id='root').find_all('h4')
                l=[]
                for i in dish:
                    i=i.getText()
                    l.append(i)
                dish_.append(l)
                price=soup.find_all('span',class_='sc-17hyc2s-1 fnhnBd')
                l=[]
                for i in price:
                    i=i.getText()
                    l.append(i)
                price_.append(l)
            except:
                dish_.append(0)
                price_.append(0)
        else:
            
            dish_.append(0)
            price_.append(0)


data={'Name':name_,'Contact':contact_,'Online':online_,'Title':title_,'Area':area_,'Rating':rating_,'Votes':votes_,'Add':add_,'Cuisines':cuisines_,'CF2':cf2_,'Hours':hours_,'Link':link_,'Json':json_,'Dish':dish_,'Price':price_}
df=pd.DataFrame(data)
df.to_csv('/root/Zomato_LucknowLatest.csv')






