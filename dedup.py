import streamlit as st
import pandas as pd
import re

def clean_URL(url):
    return(re.search('https?://([A-Za-z_0-9.-]+).*', url))

def process_files(badurl_file, project_file):
    badURL_df = pd.read_csv(badurl_file)
    project_df=pd.read_csv(project_file)
    badurls = []
    for i in range(len(badURL_df)):
    #    print("item", badURL_df["Main domain name"][i])
        try:
            badurls.append(clean_URL(badURL_df["Main domain name"][i]))
        except:
            pass

    good_records = []
    for i in range(len(project_df)):
    #    print(projectrecords['Main domain name'][i])
        try:
            p_url = clean_URL(project_df['Main domain name'][i])
            if p_url not in badurls:
                good_records.append(i)
        except:
            pass

        
        output_file = project_df.loc[good_records].reset_index(drop=True)
    return(output_file)


st.title("Let's remove some bad URLs")

badURLfile = st.file_uploader("Upload your badURLS")

projectfile = st.file_uploader("Upload your project records")

time_to_process = st.button("Ready to process")
if time_to_process:
    output_file = process_files(badURLfile, projectfile)


    #print(badURL_df)


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

