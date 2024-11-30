# streamlit run untrs.py
import streamlit as st
import yaml
import json
import zw

# Button to stop the app
if st.button("Stop App"):
   st.stop()  # Stops the execution of the app

# To run only once--------------
if 'hlqst' not in st.session_state:
    st.session_state.hlqst=False
if 'hlq' not in st.session_state:
    st.session_state.hlq=''

if not st.session_state.hlqst: 
   hlq=zw.find_userid()
   st.session_state.hlqst=True
   st.session_state.hlq=hlq
#-------------------------------
# To retrieve the value from session 
hlq=st.session_state.hlq

# Read config.yaml
with open('config.yaml', 'r') as f:
   confile = yaml.safe_load(f)

# Streamlit UI
st.title(f'Unterse Utility for user {hlq}')


# Create a two-column layout for local directory
coldir1, coldir2 = st.columns([3, 1], vertical_alignment="bottom")  # Adjust the proportions as needed

# Add a text input field in the left column
with coldir1:
   dir=(confile['local']['dir'])
   dir=st.text_input("Local Directory",value=dir) # default=downloads

# Add a submit button in the right column
with coldir2:
   default_dir_button=st.button("Make Default",key='1')
   if default_dir_button:
      confile['local']['dir']=dir
      with open('config.yaml', 'w') as f: yaml.dump(confile, f)


# Create a two-column layout for local file
colfile1, colfile2 = st.columns([3, 1], vertical_alignment="bottom")

# Add a text input field in the left column
with colfile1:
   file=(confile['local']['file'])
   file=st.text_input("Local File",value=file) 

# Add a submit button in the right column
with colfile2:
   default_file_button=st.button("Make Default",key='2')
   if default_file_button:
      confile['local']['file']=file
      with open('config.yaml', 'w') as f: yaml.dump(confile, f)


# Radio button from yaml
types=(confile['remote']['type'])
type=st.radio("Data Set Type:", types)

# Create a two-column layout for remote trs ds
coltrsds1, coltrsds2 = st.columns([3, 1], vertical_alignment="bottom")

# Text input for remote tersed dataset
with coltrsds1:
   remote_tersed_dataset=(confile['remote']['tersed_dataset'])
   remote_tersed_dataset=st.text_input("Remote Tersed Dataset",value=remote_tersed_dataset) 

# Add a submit button in the right column
with coltrsds2:
   default_trs_ds_button=st.button("Make Default",key='3')
   if default_trs_ds_button:
      confile['remote']['tersed_dataset']=file
      with open('config.yaml', 'w') as f: yaml.dump(confile, f)

# Create a two-column layout for remote untrs ds
coluntrsds1, coluntrsds2 = st.columns([3, 1], vertical_alignment="bottom")

# Text input for remote untersed dataset
with coluntrsds1:
   remote_untersed_dataset=(confile['remote']['untersed_dataset'])
   remote_untersed_dataset=st.text_input("Remote UnTersed Dataset",value=remote_untersed_dataset) 

# Add a submit button in the right column
with coluntrsds2:
   default_untrs_ds_button=st.button("Make Default",key='4')
   if default_untrs_ds_button:
      confile['remote']['untersed_dataset']=file
      with open('config.yaml', 'w') as f: yaml.dump(confile, f)



edit = st.toggle("Edit File in VSCode")

if edit:
   st.write("Edit in VSCode") #dxr

submit=st.button("Submit")

if submit:
   st.write("Hello")

exit()
