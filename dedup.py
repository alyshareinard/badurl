import streamlit as st
import pandas as pd
import re

def clean_URL(url):

    try:
        url = str(url)
        clean = re.match('https?://([A-Za-z_0-9.-]+).*', url).group(0)
        return(clean)
    except:
        return("")

def process_files(badurl_file, project_file):
    badURL_df = pd.read_csv(badurl_file)
    project_df=pd.read_csv(project_file)
    badurls = []
    for i in range(len(badURL_df)):
    #    print("item", badURL_df["Main domain name"][i])

        badurls.append(clean_URL(badURL_df["Website"][i]))

    print("badURLS", badurls)
    good_records = []
    for i in range(len(project_df)):
    #    print(projectrecords['Main domain name'][i])
        if 'Website' not in project_df:
            st.write("table must have column header 'Website'")
#        print(type(project_df['Website'][i]))
        p_url = clean_URL(project_df['Website'][i])
        if p_url == "" or p_url not in badurls:
            good_records.append(i)


    output_file = project_df.loc[good_records].reset_index(drop=True)
    return(output_file)


st.title("Let's remove some bad URLs")


#st.write("Upload your bad URL file here")
badURLfile = st.file_uploader("Upload your badURLS")

#st.write("Upload your project file here")
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

