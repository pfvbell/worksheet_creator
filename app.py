import streamlit as st
import numpy as np
import pandas as pd
# import aspose.words as aw
from htmldocx import HtmlToDocx
from bing_image_downloader import downloader
import os

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

if learn_text:

    with st.spinner(text='In progress'):

        # Define Question Generator
        qg = QuestionGenerator()
        qa_list = qg.generate(
            learn_text, 
            num_questions=5, 
            answer_style='all'
        )

        questions = [text['question'] for text in qa_list]
        st.text(qa_list)

        ### Add Model to create Questions here ###

        # st.write(st.session_state.knowledge)

        ### Select Subject ###


        ### Select Age slider - lowest and highest ###

        add_slider = st.slider(
            'What reading ages do you want to cater for?',
            5, 18, (2, 18)
        )

        # Generate Comprehension Questions


        ls_technique = st.multiselect('What Learning Science technique do you want to use?', ['Writing Revolution', 'Dual Coding'])

        query_string = worksheet_title
        downloader.download(query_string, limit=2,  output_dir='images', adult_filter_off=False, force_replace=False, timeout=60, verbose=True)
        # More options here: https://pypi.org/project/bing-image-downloader/

        ### Select word or PDF ###

        f = open('worksheet.html','w')

        # folder path
        dir_path = f'images/{query_string}'

        # list to store files
        res = []

        # Iterate directory
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                res.append(path)
        print(res)

        #<img src="images/{query_string}/Image_1.jpg" alt="Image 1">

        worksheet_head = f"""<html>
        <head>
        <style>
        </style>
        </head>
        <h1>{worksheet_title}</h1>
        <body>
        <img src="images/{query_string}/{res[0]}" alt="Image 1" style="float:left;width:15px;height:15px;"
        <img src="images/{query_string}/{res[1]}" alt="Image 2" style="float:right;width:15px;height:15px;">
        <p>Read this text ... </p>
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
