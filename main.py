import streamlit as st 
from PIL import Image  # opening images
import numpy as np 
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
st.title("Paper Checker App")

def get_gemini_response(input,image):
    model = genai.GenerativeModel('gemini-pro-vision')

    response = model.generate_content(
        [
            input,image[0]
        ]
    )
    
    return response.text


def input_image_setup(upload_file):
    if upload_file is not None:
        bytes_data = upload_file.getvalue()
        image_part = [
            {
                "mime_type":upload_file.type,
                "data":bytes_data
            }
        ]
        return image_part
    

select_upload_image = st.selectbox('Select Image:',[None,'In Camera','In Gallery',])

def main(input_prompt,image):
    st.subheader("Quesion Paper Image:")
    input_image = Image.open(image)
    st.image(input_image,width=400)
    if image:
       if st.button("Calculate the Marks:"):
            with st.spinner("Please Wait test is checking..."):
                image_data = input_image_setup(image)
                respose=get_gemini_response(input_prompt,image_data)
                st.header("Total Marks with solution")
                # print(respose)
                st.markdown(respose)




input_prompt = """
you are a math teacher.your job is to check the student test then give them marks.check each step of the solution carefully.you also have to apply your own logic to each step of the student solution.also keep in mind that what is written with the  blue/black marker  will be question or heading.the steps that are wrong are also cut marks.it should also be mentioned which step is wrong.finally total marks calculate and show as many steps as  a list rather than a paragraph then 
response format bellow:
**Question [No]:**\n
    **Step [No]:=... **\n
    **Step n [No]=... **\n
    **total marks:= [marks]**
**total Marks:  ** \\sum of all marks


"""


if select_upload_image == 'In Gallery':
    image = st.file_uploader('enter a image')
    if image:
        main(input_prompt=input_prompt,image=image)
        
    
elif select_upload_image == 'In Camera':
    picture = st.camera_input('image input')
    if picture:
        main(input_prompt=input_prompt,image=picture)

else:
    st.markdown('Please select the Image method')


# input_prompt = """

# # You are a expert in math teacher.your task is check peper and calculate total marks of test with the mistake of test.each question check your resposibilty,respose type like below format 
# # 1. step right and assign marks
# # 2. step wrong and cut the marks
# # ``````
# # ``````
# # finally total marks of show 


# """
    



   
