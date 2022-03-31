import streamlit as st
import pandas as pd
import re

def clean_URL(url):
    return(re.search('https?://([A-Za-z_0-9.-]+).*', url))



st.title("Hi Marta")

badURLfile = st.file_uploader("Upload your badURLS")
badURL_df = pd.read_csv(badURLfile)


projectrecords = pd.read_csv(st.file_uploader("Upload your project records"))



#print(badURL_df)

badurls = []
for i in range(len(badURL_df)):
#    print("item", badURL_df["Main domain name"][i])
    try:
        badurls.append(clean_URL(badURL_df["Main domain name"][i]))
    except:
        pass

good_records = []
for i in range(len(projectrecords)):
#    print(projectrecords['Main domain name'][i])
    try:
        p_url = clean_URL(projectrecords['Main domain name'][i])
        if p_url not in badurls:
            good_records.append(i)
    except:
        pass

    
    output_file = projectrecords.loc[good_records].reset_index(drop=True)


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(output_file)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
)

