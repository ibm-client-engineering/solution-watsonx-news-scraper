import pandas as pd
import streamlit as st
import time
from Webscraper_tools.Webscrape import *
from Webscraper_tools.Watsonx_connection import single_article_summary, get_full_summary

st.set_page_config(layout="wide")
st.title("News Analysis with Watson:blue[x]")


#Column populating function
def article_click(article_id) :
   st.session_state['button_clicked'] = True
   st.session_state['article_id'] = article_id

def populate_columns() :
   
   st.session_state['selected'] = True
   st.session_state['button_clicked'] = False

def refresh() :
   do_webscrape.clear()
   scrape_cnbc.clear()
   scrape_cnn.clear()
   st.session_state["summary_try"] = False

def run_wx_single(df, i) :
   start_time = time.time()
   st.session_state['analysis_run'][i] = 1
   with col2:
      with st.spinner("Doing watson:blue[x] analysis") :
         single_article_summary(df, i)
      st.success(f"Completed Analysis in {time.time() - start_time} seconds", icon="✅")

def render_df() :
   datfram = pd.DataFrame(df.iloc[st.session_state['article_id'], 4:12]).T
   _, num_cols = datfram.shape
   sentiment_to_emoji = {"Falling": ":arrow-down-small:", "Decrease": ":arrow-down-small:", "Worse": ":arrow-down-small:", "Worst": ":arrow-down-small:", "Increase": ":arrow-up-small:", "Rising": ":arrow-up-small:", "Better": ":arrow-up-small:"} 
   for i in range(num_cols) :
      if datfram.iloc[0, i] in sentiment_to_emoji.keys() :
         datfram.iloc[0, i] = datfram.iloc[0, i] + " " + sentiment_to_emoji[datfram.iloc[0, i]]
   st.dataframe(datfram)

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




#Program
df = do_webscrape()
num_articles, _ = df.shape
if "summary_success" not in st.session_state :
   st.session_state["summary_success"] = False

#Summary Dashboard (commented out for now the prompting is broken)
if "summary_try" not in st.session_state or not st.session_state["summary_try"]:
   st.session_state["summary_try"] = True
   st.session_state["summary_success"] = get_full_summary(df)

if st.session_state['summary_success'] :
   for cat in df.Category.unique() :
      #print("Category: " + cat)
      st.write("**" + str(cat) + "**")
      for _, row_in_category in df.loc[df["Category"] == cat].iterrows() :
         #print(row_in_category)
         if row_in_category["Summary"] :
            st.write("- " + row_in_category["Summary"])
else :
   st.write("Summary retrieval failure")

st.selectbox("Select a news source", ("CNN", "CNBC"), on_change=populate_columns, key="source_selection", index=None, placeholder="News Source")
col1, col2 = st.columns([.3, .7])
if 'analysis_run' not in st.session_state :
   st.session_state['analysis_run'] = [0] * num_articles

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
      st.subheader(df.iloc[st.session_state['article_id']]['Title'])
      st.caption(df.iloc[st.session_state['article_id']]['Date'].strftime('Published %B %d, %Y at %I:%M %p %Z'))
      st.write(df.iloc[st.session_state['article_id']]['Text'])
      if st.session_state['analysis_run'][st.session_state['article_id']] == 1 :
         #render_df()
         df.iloc[st.session_state['article_id']]['Multi-Point Summary']
      else :
         st.button("Run Watson:blue[x] Analysis", on_click=run_wx_single, args=(df, st.session_state['article_id']))
      