import streamlit as st
import numpy as np
import pandas as pd
# import aspose.words as aw
from htmldocx import HtmlToDocx
from bing_image_downloader import downloader
import os
from PIL import Image

from questiongenerator import QuestionGenerator

import base64
import os
import json
import pickle
import uuid
import re
import shutil

st.title('Pedagogical.')
st.subheader('🔥 Worksheet-Creator Prototype 🔥')


worksheet_title = st.text_input("Insert Worksheet Title", key="w_Title")

learn_text = st.text_input("Insert what you want your students to learn", key="knowledge")

ls_technique = st.multiselect('What do you want your students to practice?', ['Writing', 'Knowledge'])
downloaded = False

if learn_text:
    if downloaded == False:
        with st.spinner(text='In progress'):

            # Define Question Generator
            qg = QuestionGenerator()
            qa_list = qg.generate(
                learn_text, 
                num_questions=5, 
                answer_style='all',
                use_evaluator = False
            )

            questions = [text['question'] for text in qa_list]

            # Make sure we don't have any duplicates.
            questions = list(set(questions))  


            query_string = worksheet_title
            downloader.download(query_string, limit=1,  output_dir='images', adult_filter_off=False, force_replace=False, timeout=60, verbose=True)
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

            image1 = Image.open(f'images/{query_string}/{res[0]}')
            image1 = image1.resize((80, 80))
            image1.save(f'images/{query_string}/{res[0]}')

            worksheet_head = f"""<html>
            <head>
            <style>
            </style>
            </head>
            <h1>{worksheet_title}</h1>
            <body>
            <p>Name ......... </p>
            <img src="images/{query_string}/{res[0]}" alt="Image 1" style="float:left;width:15px;height:15px;"
            <p><b>Read this text and highlight the key words ... </b></p>
            <p>{learn_text}</p>
            <p><b>And now answer the following questions ! </b> <br></p>"""

            qp = [question + '<br> ................................................. </p>' for question in questions]
            worksheet_questions = '<p>'.join(qp)

            worksheet_storyboard = """<p><b>Draw a picture of the text you have read below ... </b></p>
                    <svg width="400" height="180">
                    <rect x="50" y="20" width="300" height="150"
                    style="fill:blue;stroke:pink;stroke-width:5;fill-opacity:0.1;stroke-opacity:0.9" />
                    </svg>"""

            worksheet_writing_rev = """
            <p> <b> Complete the following sentences! <br></b>
            1. Write a sentence about the text above using because <br>…………………………………………………………………<br>
            2. Write a sentence about the text above using but <br>…………………………………………………………………<br>
            3. Write a sentence about the text above using so <br>…………………………………………………………………<br>
            </p>
            """

            worksheet_end = """</body>
            </html>"""


            if ls_technique == 'Knowledge':
                full_worksheet = worksheet_head + worksheet_questions + worksheet_storyboard + worksheet_end
            else: 
                full_worksheet = worksheet_head + worksheet_questions + worksheet_writing_rev + worksheet_end

            f.write(full_worksheet)
            f.close()

            new_parser = HtmlToDocx()
            new_parser.parse_html_file("worksheet.html", "worksheet")


            file_path = 'worksheet.docx'
            with open(file_path,"rb") as f:
                base64_word = base64.b64encode(f.read()).decode('utf-8')

            with open("worksheet.docx", "rb") as word_file:
                wordbyte = word_file.read()

            # Remove directory of images
            shutil.rmtree(dir_path) 

            downloaded = st.download_button(label="Download Custom Worksheet", 
            data=wordbyte,
            file_name="worksheet_doc_test.docx",
            mime='application/octet-stream')
