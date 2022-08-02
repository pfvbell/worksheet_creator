import streamlit as st
import numpy as np
import pandas as pd
# import aspose.words as aw
from htmldocx import HtmlToDocx

from questiongenerator import QuestionGenerator

import base64
import os
import json
import pickle
import uuid
import re

st.title('Pedagogical.')
st.subheader('🔥 Worksheet-Creator Prototype 🔥')


worksheet_title = st.text_input("Insert Worksheet Title", key="w_Title")

learn_text = st.text_input("Insert what you want your students to learn", key="knowledge")

# Define Question Generator
qg = QuestionGenerator()
qa_list = qg.generate(
    learn_text, 
    num_questions=10, 
    answer_style='all'
)

questions = [text['question'] for text in qa_list]
st.text(questions[0])
st.text(questions[1])

### Add Model to create Questions here ###

st.write(st.session_state.knowledge)

### Select Subject ###


### Select Age slider - lowest and highest ###

add_slider = st.slider(
    'What reading ages do you want to cater for?',
    5, 18, (2, 18)
)

# Generate Comprehension Questions


ls_technique = st.multiselect('What Learning Science technique do you want to use?', ['Writing Revolution', 'Dual Coding'])

### Select word or PDF ###

f = open('worksheet.html','w')

worksheet_head = f"""<html>
<head></head>
<h1>{worksheet_title}</h1>
<body><p>Read this text ... </p>
<p>{learn_text}</p>"""

qp = [question + '</p>' for question in questions]
worksheet_questions = '<p>'.join(qp)


worksheet_end = """</body>
</html>"""

full_worksheet = worksheet_head + worksheet_questions + worksheet_end

f.write(full_worksheet)
f.close()

new_parser = HtmlToDocx()
new_parser.parse_html_file("worksheet.html", "worksheet")

# doc = aw.Document("worksheet.html")
# doc.save("worksheet.docx")

# # word first #
# # create document object
# doc = aw.Document()

# # create a document builder object
# builder = aw.DocumentBuilder(doc)

# # add text to the document
# builder.write(st.session_state.knowledge)

# doc.save("current_doc.docx")

# st.download_button('Download file', doc)

file_path = 'worksheet.docx'
with open(file_path,"rb") as f:
    base64_word = base64.b64encode(f.read()).decode('utf-8')


# word_display = f'<iframe src="data:application/docx;base64,{base64_word}" width="800" height="800" type="application/docx"></iframe>'

# st.markdown(word_display, unsafe_allow_html=True)

# FOr downloading word doc or pdf: https://towardsdatascience.com/display-and-download-pdf-in-streamlit-a-blog-use-case-5fc1ac87d4b1

with open("worksheet.docx", "rb") as word_file:
    wordbyte = word_file.read()

st.download_button(label="Download Custom Worksheet", 
        data=wordbyte,
        file_name="worksheet_doc_test.docx",
        mime='application/octet-stream')
