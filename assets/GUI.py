import pandas as pd
import streamlit as st
from Webscrape import *

st.set_page_config(layout="wide")
st.title("Watson:blue[x] Webscraper")


#Column populating function
def article_click(article_id) :
   st.session_state['button_clicked'] = True
   st.session_state['article_id'] = article_id

def populate_columns() :
   
   st.session_state['selected'] = True
   st.session_state['button_clicked'] = False

def do_webscrape() :
    cnn_articles = scrape_cnn()
    cnbc_articles = scrape_cnbc()
    combined_articles = cnn_articles + cnbc_articles

    return create_df(combined_articles)

def refresh() :
   
   create_df.clear()
   

# tab1, tab2 = st.tabs(['CNN', 'CNBC'])
if 'selected' not in st.session_state :
   st.session_state['selected'] = False
if 'button_clicked' not in st.session_state :
   st.session_state['button_clicked'] = False
if 'article_id' not in st.session_state :
   st.session_state['article_id'] = -1
topcol1, topcol2 = st.columns([.85, .1])
with topcol2 :
   st.button("Refresh Webscrape", on_click=refresh, key="refresh_button")
st.selectbox("Select a news source", ("CNN", "CNBC"), on_change=populate_columns, key="source_selection", placeholder="News Source")
col1, col2 = st.columns([.3, .7])



#Program
df = do_webscrape()


if st.session_state['selected'] :
    source_df = df.loc[df['Source'] == st.session_state['source_selection']]
    with col1:
        st.title("Headlines")
        with st.container(height=600, border=False) :
            for index, row in source_df.iterrows() :
                if index == st.session_state['article_id'] :
                    st.button(row['Title'], on_click=article_click, args=(index,), type='primary')
                else:
                    st.button(row['Title'], on_click=article_click, args=(index,))

if st.session_state['button_clicked'] :
    with col2:
      st.write(df.iloc[st.session_state['article_id']]['Text'])
      st.table(df.iloc[st.session_state['article_id'], 4:12])


