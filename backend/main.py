# TODO: (STATUS: DITCHED) Browser Extension for tracking user's flipkart browsing session and purchase history
# TODO: Discuss on showing extra Product Details like size, color, etc
# TODO: Filter (Budget, Brand, Size, Color, etc)
# TODO: Improve tagging using chain of thought prompting
# TODO: Social Media Trends using https://github.com/acheong08/EdgeGPT
# TODO: Switch over to official OpenAI API

from typing import Union
import instaloader
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from revChatGPT.V1 import Chatbot
import os
import openai
from dotenv import load_dotenv
import glob
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import openai
import requests
import json
from twilio.rest import Client
import datetime

# chatbot = Chatbot(config={
#   "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJzd2NpaXRnaHlAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWV9LCJodHRwczovL2FwaS5vcGVuYWkuY29tL2F1dGgiOnsidXNlcl9pZCI6InVzZXItdDkydFZ2UVducDgyQUlHZ2Z4bEM2MmpUIn0sImlzcyI6Imh0dHBzOi8vYXV0aDAub3BlbmFpLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMzQxNDkyNDM2MjMxNzQ4OTAxMCIsImF1ZCI6WyJodHRwczovL2FwaS5vcGVuYWkuY29tL3YxIiwiaHR0cHM6Ly9vcGVuYWkub3BlbmFpLmF1dGgwYXBwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2OTA4NzA1MDAsImV4cCI6MTY5MjA4MDEwMCwiYXpwIjoiVGRKSWNiZTE2V29USHROOTVueXl3aDVFNHlPbzZJdEciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIG1vZGVsLnJlYWQgbW9kZWwucmVxdWVzdCBvcmdhbml6YXRpb24ucmVhZCBvcmdhbml6YXRpb24ud3JpdGUgb2ZmbGluZV9hY2Nlc3MifQ.pJL7L1WMfymxNvfFjMUmej-4y5syM8CIVEy9e6JU_mCXkTttJBjHysWyARePFDzp8nNxKYjYRpyYa08v6JhPLoaSOmWSBCP5LI2_MW7lp23ET2CyAmPZLvg5HiwVH-JaXYHsSvlPxRPsJ68aJBE59pr4bXFV3gYa_o-A7pbtBw0RZcOWgYrJU2E4dgCWQyJ-vgbBLgv7gIbo9HmNqfvid-rXJjGvoYeJlmgCcv8dQ7ROA3RyC2PdvBlwY--37AldIw6AUMAi_Hr7LdvOTsw-vO8zebo4C263kZqDpzbar5BkMH6d5caojOlaGg85TXCs1JkYUiCYvetH1-C1D4YmgA"
# })
# convo_id = ""

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_API_KEY")


twilio_sid=os.getenv("TWILIO_SID")
twilio_auth_token=os.getenv("TWILIO_AUTH_TOKEN")
twilio_client=Client(twilio_sid,twilio_auth_token)
user_phone=""

user_details={
        'age' : '',
        'location' : '',
        'gender' : '',
        'user_instructions' : '',
        'userQuery' : '',
        'date': str(datetime.datetime.now()),
        'budget': ''
}

empty_field_response={
    'age' : "What's your age ?",
    'location' : "what's your location (city/town/country) ?",
    'gender' : "What's your gender ?",
    'user_instructions' : 'Any specific instructions you have for the recommendations ?',
    'budget' : "What's your overall budget ?"
}

# user_details={
#                 "gender" : "Male",
#                 "userQuery" : "Suggest an outfit for a diwali party",
#                 "user_instructions" : "Don't Suggest slim fit clothes",
#                 "location" : "Mumbai",
#                 "date": "10/08/2023",
#                 "age": "23",
#                 "budget"  : "5000"
#                     }

app = FastAPI()

userData = {}

messages=[]

fashion_trends=[]

default_cart_history=["Men Solid Round Neck Polyester White T-Shirt", "Flip Flops  (Black 9)", "Flip Flops  (Navy, Grey 9)", "Solid Men Track Suit"]
cart_history=["Men Solid Round Neck Polyester White T-Shirt", "Flip Flops  (Black 9)", "Flip Flops  (Navy, Grey 9)", "Solid Men Track Suit"]

@app.on_event('startup')
def init_data():
    print("init call")
    global userData
    global default_cart_history
    userData["purchase_history"] = ["Men Solid Round Neck Polyester White T-Shirt", "Flip Flops  (Black 9)", "Flip Flops  (Navy, Grey 9)", "Solid Men Track Suit", "LUX INFERNO Men Top Thermal", "Woven Beanie", "Men Solid Black Track Pants", "Jockey Men's Cotton Shorts (SP26-0103-BLACK Black L)", "Hygear Men's Xpress Olive green Slippers_10 UK (HG-GE-1004)", "Jockey Men's Tailored Fit Cotton Thermal Long John (2420-Black-S_Black_S)", "Li-Ning Ultra IV Non-Marking Cushion Badminton Shoe (White, Navy, 9 UK, Unisex)", "Bewakoof Men's Cotton Solid Solid Black and White Half Sleeves | Round Neck | Regular Fit T-Shirt/Tee, Black, White", "GRITSTONES Anthramelange Full Sleeves High Neck T-Shirt (Large) Dark Grey", "DAMENSCH Men's Boy Shorts (DAM-WWB-SHT-TLB-M_D.Lit Brown_M)", "513 Men Acrylic Woolen Casual Winter Wear Striped Knitted Warm Premium Mufflers Black", "513 Girl's Self-Design Mufflers (jd423mufwmrn_Multicolored_Free Size)", "Eden & Ivy Women's Cotton Knee Length Regular Nightgown", "Eden & Ivy Women's Cotton Knee Length Relaxed Nightgown"]
    userData["browsing_history"] = ["Jockey SP26 Men's Super Combed Cotton Rich Regular Fit Solid Shorts with Side Pockets", "Puma Unisex-Adult Jog V3 Flip-Flop", "Woodland Men's Off Slipper", "Woodland mens Flip Flop", "Campus Men's Flip Flops", "Adidas mens Adirio Attack Slipper", "Hygear mens Xpress Slipper", "Jockey 9426 Men's Super Combed Cotton Rich Regular Fit Solid Shorts with Side Pockets", "Jockey 9411 Men's Super Combed Cotton Rich Straight Fit Solid Shorts with Side Pockets", "Hygear mens Zodiac Slipper", "Hygear mens Xpress Slipper", "Red Tape Women's Walking Shoes", "Puma Womens Reflex WNS Running Shoe", "US Polo Association mens Facundo Flip-flop", "crazymonk One Piece Monkey D Luffy Round Neck Anime T-Shirt"]
    userData["cart_history"] = default_cart_history
    global fashion_trends
    fashion_trends = open("./captions.txt", "r").readlines()
    for idx, caption in enumerate(fashion_trends):
        print(caption)
        print(type(caption))
        print(caption[-2:])
        if caption[-2:]=="\n":
            fashion_trends[idx]=caption[:-2]
            print(caption[:-2])
    print("fetched fashion trends")
    global messages
    messages=[
       {
            "role": 'system',
            "content": """You are a fashion assistant at an online fashion e-commerce website. You only speak JSON and all responses should be in JSON format strictly and the JSON Object should be of one of the following two types delimeted in angle brackets:
            1. < ASSISTANT_QUESTION_FORMAT >: The example for this format is given below enclosed in triple backticks:

            '''
            {{
                "question" : "What is the budget for your outfit"
            }}
            '''
            The value of the key "question" in  ASSISTANT_QUESTION_FORMAT should contain the question you want to ask the user

            2. < ASSISTANT_OUTPUT_FORMAT > : The example for this format given below enclosed in triple backticks:
            '''
                {{
            "recommendation": ['black colored full sleeved chinos','Red Sport Shoes'],
            "budget": "5000",
            "gender": "Male",
            "occasion": "Diwali Party"
            "assistant_notes": "The user wants a outfit for a diwali party which is an traditional event hence the clothes recommended must be traditional",
            }}
            '''
            The explanation for the values of the keys in ASSISTANT_OUTPUT_FORMAT are as follows:
            "recommendation" : This field consists the list of the recommendations that you generate. Please ensure that the recommendations is an tags of tags relating to each part of  the outfit. These tags will then be directly used to search for the items in a ecommerce site.
            "budget": The budget specified by the user. 
            "gender" : The gender of the user (male, female or unisex).
            "occasion": The occasion for which the user wants the outfit.
            "assistant _notes": These are the notes that you may generate while deciding the perfect outfit for the user.
            To specify the user's details you will be given a RFC8259 compliant json object along with the request from the user. The request json will always be in the format as shown in the example below enclosed in backticks.
            '''
                    {{
                    "past_purchases" : ["black colored full sleeved chinos","Red Sport Shoes"],
                    "browsing_history" : ["Oversized Tshirts","Red Trousers"],
                    "gender" : "Male",
                    "trends" : {0},
                    "cart_history" : {1}
                    "user_request" : "Suggest an outfit for a diwali party"
                    "user_instructions" : "Don't Suggest slim fit clothes",
                    "location" : "Mumbai",
                    "date": "10/08/2023",
                    "age": "23"
                    "budget"  : "5000"
                        }}
                '''

            Let us call this the USER_REQUEST_FORMAT.
            The explanations for the value of the keys in the User request JSON Object given in the USER_REQUEST_FORMAT format can be found below.
                    "past_purchases" : This will be an array of previous purchases of outfit items. use this to understand user's outfit preference strictly
                    "browsing_history" : This will be an array of names of the items searched by the user online in the past. Analyze this to understand the user's outfit preferences and you are strictly not supposed to recommend these names directly.
                    "gender" : This value represents the gender of the user.
                    "cart_history" : "This will be an array of product names, user has added to cart in the online ecommerce platform. from this understand what is user preferences for your recommended tags\n
                    use this to decide new tags for newer responses."
                    "trends" : This will be an array containing clothing categories currently trending among people.
                    "user_request" : This field contains the actual request from the user. It must contain the occasion for which the user is requesting an outfit. If it doesn't contain the occasion, ask for the occasion in the format for questioning ( ASSISTANT_QUESTION_FORMAT) specified before. User may have explained you the purpose of buying to try to use that as occasion for recommending
                    "user_instructions" : Some specific instructions from the user about the clothes that they wants. You are strictly supposed to follow these instructions. Do not generate responses that does not follow these instructions. You can ask for clarifications from user by asking questions in the ASSISTANT_QUESTION_FORMAT and try to ask relevant questions only.
                    "location" : User's geographic location.
                    "date": The date when the user makes a request. Use the location field's value and the date provided value to decide recommendations which can be worn in the weather in that location around this date. Also look for major events around that date in that location and make suggestions accordingly.
                    "age": The age of the user
                    "budget" : "This value determines the budget of the user. if user has specified budget value in earlier messages then, append budget value in your recommended tags strictly
                    without any deviation as this will help in efficient searchablity on e-commerce website online. for example: user budget is 5000 then add budget values acoording to approximate prices you have guessed for each outfit component
                    'Tshirt for men under 500 <this 500 here will be the approximate price of outfit component you have thought in the total budget>' as a tag recommended. assume 10000 as default total budget if not specified in messages."
                    
            If you wish to ask any question to the user. ask it as a RFC8259 compliant json object in  ASSISTANT_QUESTION_FORMAT format specified before.

            The user's request must contain the occasion for which he needs an outfit. If it does not contain the occasion assume that the outfit recommendation is for casual wear.

            While generating the response break down the problem into multiple smaller chunks. Before recommending anything, answer the below questions:
            1. What is the type of the occasion for which the user is searching a outfit. occasion may be formal, informal, traditional or casual or something else. What is the significance of the occasion and what kind of clothes do people usually wear on such occasions.
            2. What do you understand about the user's preferences from his purchasing history and browsing history. What are his preferred brands and clothing style.
            3. What do you understand from the data given about the current trends. Is the data about current trends relevant while recommending outfit for the occasion given by the user. Do the trends is relevant for occasion or should the trends be ignored?
            4. What would be an approximate price of each component of the outfit recommended? and how much should be the approximate price for each component to fit in user total budget
            5. If a user requests outfit like some personality. First think about who may be that personality and what kind of clothes does that personality usually wear and then think of some options.
            6. What are some important events/festivals around the date specified in the request in the location of the user and what outfit style may be followed. What is the usual weather at that time at that location and what kind of clothes can be worn in that weather.

            user request may be related to your old recommendations and he may be asking you to suggest something else for some item(s) you recommended earlier.
            you have to see your earlier recommended tags for those item(s) and then recommend something else for those item(s) strictly.
            for example: user request is "I didn't like shoes you recommended suggested. show something else" then you have to see your earlier recommended tags for related item and then recommend something else for this item(s) strictly. and you have to follow this strictly and return output in ASSISTANT_OUTPUT_FORMAT format strictly.

            Add the answers to the above questions in the "assistant_notes" field of the ASSISTANT_OUTPUT_FORMAT format while generating the output.
            Use the answers to these questions to recommend the outfits to the user. Do not recommend something which violates the answers of the questions given above. Make sure the outfit recommendations are complete and well coordinated including clothing,accessories and footwear.


            Please give the recommendations as a set of searchable tags which can be then searched directly on ecommerce website. Strictly append user's gender and age in every
                    recommendation you give for example if your ASSISTANT_OUTPUT_FORMAT output is '''{{
                        "recommendation" : ["tshirt", "jeans"]
                    }}''' and user's gender is "Male" and age "23" then, modify your ASSISTANT_OUTPUT_FORMAT output by appending user's "gender" to every item in recommendation array. for ex:
                    ''''{{
                        "recommendation" : ["tshirt for Men/Male age 23","jeans for Women/Female age 23"]
                    }}'''   
            Please give the recommendations as a set of searchable tags which can be then searched directly on ecommerce website. Please strictly adhere to the nature of the occasion being specified ( i.e whether it is traditional, formal etc) while recommending outfit.
            The output should always be given as a RFC8259 compliant JSON response in the ASSISTANT_OUTPUT_FORMAT format specified at the start of the message.
            Do not return anything response which are not in the 2 JSON Object formats specified at the start of the message namely: ASSISTANT_OUTPUT_FORMAT and ASSISTANT_QUESTION_FORMAT. The user's request will follow this message
            """.format(fashion_trends,cart_history)
            }
    ]
    # with open ("./temp.txt", "w") as file:
    #     file.write(str(messages) + "\n")


origins = ["http://localhost:5173", "http://localhost:4173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_influencer_posts():
    L = instaloader.Instaloader(save_metadata=False)

    # List of usernames
    usernames = ['vogueindia','fashionfloorindia','thesouledstore','__ranbir_kapoor_official__','stylebyami','gqindia']  # Add the usernames you want to download posts from
    # Loop through the usernames
    for username in usernames:
        try:
            # Load a profile
            profile = instaloader.Profile.from_username(L.context, username)
            print("Got profile")
            count =0 
            # Get the first two posts from the profile
            for post in profile.get_posts():
                # Download the post
                if not post.is_video:
                    L.download_post(post, target="posts")
                    count+=1
                    if count==2:
                        break
        except Exception as e:
            print(f"An error occurred with user {username}: {e}")
    txt_files = glob.glob(os.path.join("images", '*.txt'))
    for txt_file in txt_files:
        os.remove(txt_file)

@app.get("/")
def read_root():
    return {"Hello": "World"}


def get_product_details(product_link:str,driver):
    driver.get(product_link)
    time.sleep(2)
    return {}

def chatgpt_query(userQuery):
    global messages
    messages.append({'role' : 'user','content' : userQuery})
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=messages,
    temperature=0)
    #print(response['choices'][0]['message']['content'])
    gpt_response = json.loads(response['choices'][0]['message']['content'])
    print(gpt_response)
    if "question" in gpt_response:
        print(gpt_response["question"])
        messages.append({'role' : 'assistant','content' : json.dumps(gpt_response["question"])})
    elif "recommendation" in gpt_response:
        print(gpt_response["recommendation"])
        messages.append({'role' : 'assistant','content' : json.dumps(gpt_response["recommendation"])})
    else:
        print(gpt_response)
        messages.append({'role' : 'assistant','content' : json.dumps(gpt_response)})
    return gpt_response
    

@app.get("/items/{userQuery}")
def scrape_flipkart(age:int,location:str,gender:str,user_instructions:str,curr_date:str,userQuery:str):

    global cart_history
    user_requests = {
		  "past_purchases" : ["black colored full sleeved chinos","Red Sport Shoes"],
		  "browsing_history" : ["Oversized Tshirts","Red Trousers"],
          "cart_histroy" : cart_history,
          "age" : age,
		  "gender" : gender,
		  "trends" : ["Oversized Printed Tshirts", "Ripped Jeans"],
		  "user_request" : userQuery,
		  "user_instructions" : user_instructions,
		  "location" : location,
		  "date": curr_date,
		  "budget"  : "10000"
        }
    
    user_message = {
        "role": "user",
        "content": json.dumps(user_requests)
    }

    messages.append(user_message)
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", messages=messages)
    print(chat_completion)
    gpt_response = json.loads(chat_completion['choices'][0]['message']['content'])
    print(gpt_response);
    if "question" in gpt_response:
        messages.append({'role' : 'assistant','content' : json.dumps(gpt_response["question"])})
        return gpt_response
    elif "recommendation" in gpt_response:
        print(gpt_response["recommendation"])
        messages.append({'role' : 'assistant','content' : json.dumps(gpt_response["recommendation"])})
    elif type(gpt_response)==list:
        print(gpt_response)
        messages.append({'role' : 'assistant','content' : json.dumps(gpt_response)})
    else:
        messages.append({'role' : 'assistant','content' : json.dumps(gpt_response)})
        return {"question" : gpt_response}
    # Call ChatGPT for flipkart search
    # print(chat_completion)
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    response={"recommendations": []}

    # Get the products from flipkart
    for search_query in (gpt_response["recommendation"] if "recommendation" in gpt_response else gpt_response):
        try:
            driver.get(f"https://www.flipkart.com/search?q={search_query}")
            product_cards = driver.find_elements(By.CLASS_NAME, "_373qXS")
            product_description={"search_query" : search_query}
            for product_card in product_cards:
                try:
                    if (product_card.find_element(By.CLASS_NAME, "_2I5qvP").find_element(By.TAG_NAME, "span").text):
                        print("Sponsored")
                except:
                    product_description["product_link"] = str(product_card.find_element(By.TAG_NAME, "a").get_attribute("href"))
                    product_description["product_name"] = str(product_card.find_element(By.CLASS_NAME, "IRpwTa").text)
                    product_description["product_price"] = product_card.find_element(By.CLASS_NAME, "_30jeq3").text
                    product_description["image_link"] = str(product_card.find_element(By.TAG_NAME, "img").get_attribute("src"))
                    break
            if product_description["product_link"]!="":
                response["recommendations"].append(product_description)
        except Exception as e:
            print(e)
            print("Outer except")
            pass

    # get_product_details(product_description["product_link"],driver)
    driver.close()
    print(response)
    return response
    

@app.get("/regenerate-item")
def regenerate_item(search_query, product_name):
    messages.append({'role' : 'system','content' : f'''your recomendation had {search_query} in it and item based on that searchable tag fetched from online e-commerce store was not liked by user and fetched product name is {product_name}.\n
    you have to change this recommendation after analyzing the reasons why this tag couldn't have worked and this product name got recommended and generate new one afterwards. you only speak JSON and have to return the response in format : """"{{"tag" : "new tag recommended by you}}""" strictly without any deviation'''})
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", messages=messages)
    print(chat_completion)
    gpt_response = json.loads(chat_completion['choices'][0]['message']['content'])
    print(gpt_response)
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(f"https://www.flipkart.com/search?q={gpt_response['tag']}")
    product_cards = driver.find_elements(By.CLASS_NAME, "_373qXS")
    product_description={"search_query" : search_query}
    for product_card in product_cards:
        try:
            if (product_card.find_element(By.CLASS_NAME, "_2I5qvP").find_element(By.TAG_NAME, "span").text):
                print("Sponsored")
        except:
            product_description["product_link"] = str(product_card.find_element(By.TAG_NAME, "a").get_attribute("href"))
            product_description["product_name"] = str(product_card.find_element(By.CLASS_NAME, "IRpwTa").text)
            product_description["product_price"] = product_card.find_element(By.CLASS_NAME, "_30jeq3").text
            product_description["image_link"] = str(product_card.find_element(By.TAG_NAME, "img").get_attribute("src"))
            break
    return {"recommendations": [product_description]}

@app.get("/clear")
def clear():
    global messages
    global fashion_trends
    global userData
    global cart_history
    cart_history=default_cart_history
    print(fashion_trends)
    messages.clear()
    messages = [
            {
                    "role": 'system',
                    "content": """You are a fashion assistant at an online fashion e-commerce website. You only speak JSON and all responses should be in JSON format strictly and the JSON Object should be of one of the following two types delimeted in angle brackets:
        1. < ASSISTANT_QUESTION_FORMAT >: The example for this format is given below enclosed in triple backticks:

        '''
        {{
            "question" : "What is the budget for your outfit"
        }}
        '''
        The value of the key "question" in  ASSISTANT_QUESTION_FORMAT should contain the question you want to ask the user

        2. < ASSISTANT_OUTPUT_FORMAT > : The example for this format given below enclosed in triple backticks:
        '''
            {{
        "recommendation": ['black colored full sleeved chinos','Red Sport Shoes'],
        "budget": "5000",
        "gender": "Male",
        "occasion": "Diwali Party"
        "assistant_notes": "The user wants a outfit for a diwali party which is an traditional event hence the clothes recommended must be traditional",
        }}
        '''
        The explanation for the values of the keys in ASSISTANT_OUTPUT_FORMAT are as follows:
        "recommendation" : This field consists the list of the recommendations that you generate. Please ensure that the recommendations is an tags of tags relating to each part of  the outfit. These tags will then be directly used to search for the items in a ecommerce site.
        "budget": The budget specified by the user. 
        "gender" : The gender of the user (male, female or unisex).
        "occasion": The occasion for which the user wants the outfit.
        "assistant _notes": These are the notes that you may generate while deciding the perfect outfit for the user.
        To specify the user's details you will be given a RFC8259 compliant json object along with the request from the user. The request json will always be in the format as shown in the example below enclosed in backticks.
        '''
                {{
                "past_purchases" : ["black colored full sleeved chinos","Red Sport Shoes"],
                "browsing_history" : ["Oversized Tshirts","Red Trousers"],
                "gender" : "Male",
                "trends" : {0},
                "cart_history" : {1},
                "user_request" : "Suggest an outfit for a diwali party"
                "user_instructions" : "Don't Suggest slim fit clothes",
                "location" : "Mumbai",
                "date": "10/08/2023",
                "age": "23"
                "budget"  : "5000"
                    }}
            '''

        Let us call this the USER_REQUEST_FORMAT.
        The explanations for the value of the keys in the User request JSON Object given in the USER_REQUEST_FORMAT format can be found below.
                "past_purchases" : This will be an array of previous purchases of outfit items. use this to understand user's outfit preference strictly
                "browsing_history" : This will be an array of names of the items searched by the user online in the past. Analyze this to understand the user's outfit preferences and you are strictly not supposed to recommend these names directly.
                "cart_history" : "This will be an array of product names, user has added to cart in the online ecommerce platform. from this understand what is user preferences for your recommended tags\n
                use this to decide new tags for newer responses."
                "gender" : This value represents the gender of the user.
                "trends" : This will be an array containing clothing categories currently trending among people.
                "user_request" : This field contains the actual request from the user. It must contain the occasion for which the user is requesting an outfit. If it doesn't contain the occasion, ask for the occasion in the format for questioning ( ASSISTANT_QUESTION_FORMAT) specified before. User may have explained you the purpose of buying to try to use that as occasion for recommending
                "user_instructions" : Some specific instructions from the user about the clothes that they wants. You are strictly supposed to follow these instructions. Do not generate responses that does not follow these instructions. You can ask for clarifications from user by asking questions in the ASSISTANT_QUESTION_FORMAT and try to ask relevant questions only.
                "location" : User's geographic location.
                "date": The date when the user makes a request. Use the location field's value and the date provided value to decide recommendations which can be worn in the weather in that location around this date. Also look for major events around that date in that location and make suggestions accordingly.
                "age": The age of the user
                "budget" : "This value determines the budget of the user. if user has specified budget value in earlier messages then, append budget value in your recommended tags strictly \n
                without any deviation as this will help in efficient searchablity on e-commerce website online. for example: user budget is 5000 then add budget values acoording to approximate prices you have guessed for each outfit component\n
                'Tshirt for men under 500 <this 500 here will be the approximate price of outfit component you have thought in the total budget>' as a tag recommended. assume 10000 as default total budget if not specified in messages."
                
        If you wish to ask any question to the user. ask it as a RFC8259 compliant json object in  ASSISTANT_QUESTION_FORMAT format specified before.

        The user's request must contain the occasion for which he needs an outfit. If it does not contain the occasion assume that the outfit recommendation is for casual wear.

        While generating the response break down the problem into multiple smaller chunks. Before recommending anything, answer the below questions:
        1. What is the type of the occasion for which the user is searching a outfit. occasion may be formal, informal, traditional or casual or something else. What is the significance of the occasion and what kind of clothes do people usually wear on such occasions.
        2. What do you understand about the user's preferences from his purchasing history and browsing history. What are his preferred brands and clothing style.
        3. What do you understand from the data given about the current trends. Is the data about current trends relevant while recommending outfit for the occasion given by the user. Do the trends is relevant for occasion or should the trends be ignored?
        4. What would be an approximate price of each component of the outfit recommended? and how much should be the approximate price for each component to fit in user total budget
        5. If a user requests outfit like some personality. First think about who may be that personality and what kind of clothes does that personality usually wear and then think of some options.
        6. What are some important events/festivals around the date specified in the request in the location of the user and what outfit style may be followed. What is the usual weather at that time at that location and what kind of clothes can be worn in that weather.
    
        Add the answers to the above questions in the "assistant_notes" field of the ASSISTANT_OUTPUT_FORMAT format while generating the output.
        Use the answers to these questions to recommend the outfits to the user. Do not recommend something which violates the answers of the questions given above. Make sure the outfit recommendations are complete and well coordinated including clothing,accessories and footwear.

        Please give the recommendations as a set of searchable tags which can be then searched directly on ecommerce website. Strictly append user's gender and age in every \n
        recommendation you give for example if your ASSISTANT_OUTPUT_FORMAT output is '''{{
            "recommendation" : ["tshirt", "jeans"]
        }}''' and user's gender is "Male" and age "23" then, modify your ASSISTANT_OUTPUT_FORMAT output by appending user's "gender" to every item in recommendation array. for ex:
        '''{{
            "recommendation" : ["tshirt for Men/Male age 23","jeans for Women/Female age 23"]
        }}'''       
        . Please strictly adhere to the nature of the occasion being specified ( i.e whether it is traditional, formal etc) while recommending outfit. The output should always be given as a \n
        RFC8259 compliant JSON response in the ASSISTANT_OUTPUT_FORMAT format specified at the start of the message. Do not return anything response which are not \n
        in the 2 JSON Object formats specified at the start of the message namely: ASSISTANT_OUTPUT_FORMAT and ASSISTANT_QUESTION_FORMAT. The user's request will follow this message
        you can use emojis in the responses
        """.format(fashion_trends,cart_history)}
    ]

    userData={
        'age' : '',
        'location' : '',
        'gender' : '',
        'user_instructions' : '',
        'userQuery' : '',
        'date': str(datetime.datetime.now()),
        'budget': ''
        }

    # with open ("./temp.txt", "w") as file:
    #     file.write(str(messages) + "\n")
    return { "status": "success" }

@app.get("/cart-history/{product_name}")
def save_cart_history(product_name: str):
    print(product_name)
    global cart_history
    cart_history.append(product_name)
    return { "status": "success" }


def send_message(body_text):
    global twilio_client
    global user_phone
    print(user_phone,twilio_client)
    twilio_client.messages.create(
        from_=f"whatsapp:+14155238886", body=body_text, to=f"whatsapp:+91{user_phone}"
    )

def find_empty_user_details_field():
    for key, value in user_details.items():
        if value=='' and key!='userQuery':
            return key
    return ''

def check_user_details_empty():
    res=True
    for key, value in user_details.items():
        if value!='':
            res=False
    return res


def scrape_flipkart_whatsapp(age:int,location:str,gender:str,user_instructions:str,curr_date:str,userQuery:str):
    global cart_history
    user_requests = {
		  "past_purchases" : ["black colored full sleeved chinos","Red Sport Shoes"],
		  "browsing_history" : ["Oversized Tshirts","Red Trousers"],
          "cart_history" : cart_history,
          "age" : age,
		  "gender" : gender,
		  "trends" : ["Oversized Printed Tshirts", "Ripped Jeans"],
		  "user_request" : userQuery,
		  "user_instructions" : user_instructions,
		  "location" : location,
		  "date": curr_date,
		  "budget"  : "10000"
        }
    
    user_message = {
        "role": "user",
        "content": json.dumps(user_requests)
    }

    messages.append(user_message)
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", messages=messages)
    print(chat_completion)
    gpt_response=""
    try:
        gpt_response = json.loads(chat_completion['choices'][0]['message']['content'])
    except:
        gpt_response=chat_completion['choices'][0]['message']['content']
    print(gpt_response)
    print(type(gpt_response))
    print(type(gpt_response)==str)
    if "question" in gpt_response:
        messages.append({'role' : 'assistant','content' : json.dumps(gpt_response["question"])})
        print(gpt_response["question"])
        return gpt_response["question"]
    elif "recommendation" in gpt_response:
        print(gpt_response["recommendation"])
        messages.append({'role' : 'assistant','content' : json.dumps(gpt_response["recommendation"])})
    elif type(gpt_response)==list:
        print(gpt_response)
        messages.append({'role' : 'assistant','content' : json.dumps(gpt_response)})
    elif type(gpt_response)==str:
        print(gpt_response)
        messages.append({'role' : 'assistant','content' : json.dumps(gpt_response)})
        return gpt_response
    # Call ChatGPT for flipkart search
    # print(chat_completion)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    response={"recommendations": []}

    # Get the products from flipkart
    for search_query in (gpt_response["recommendation"] if "recommendation" in gpt_response else gpt_response):
        print("hjfsjhkd")
        try:
            driver.get(f"https://www.flipkart.com/search?q={search_query}")
            product_cards = driver.find_elements(By.CLASS_NAME, "_373qXS")
            print(product_cards)
            product_description={"search_query" : search_query}
            for product_card in product_cards:
                try:
                    if (product_card.find_element(By.CLASS_NAME, "_2I5qvP").find_element(By.TAG_NAME, "span").text):
                        print("Sponsored")
                except:
                    product_description["product_link"] = str(product_card.find_element(By.TAG_NAME, "a").get_attribute("href"))
                    product_description["product_name"] = str(product_card.find_element(By.CLASS_NAME, "IRpwTa").text)
                    product_description["product_price"] = product_card.find_element(By.CLASS_NAME, "_30jeq3").text
                    product_description["image_link"] = str(product_card.find_element(By.TAG_NAME, "img").get_attribute("src"))
                    # print(product_description)
                    url = 'https://t.ly/api/v1/link/shorten'
                    print(product_description["product_link"])
                    payload = {
                        "long_url": product_description["product_link"],
                        "domain": "https://t.ly/",
                        "expire_at_datetime": "2035-01-17 15:00:00",
                        "description": "Flipkart Link",
                        "public_stats": True
                    }
                    headers = {
                    'Authorization': 'Bearer AQZhY6BHbKsneCcZBR8lvXRgELGgZ6WesoAstsFzzzmJPSxfIEiM8iWjEOIR',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                    }

                    res = requests.request('POST', url, headers=headers, json=payload)
                    # print(response)
                    # print(response.json())
                    # print(response.json()["short_url"])
                    data=res.json()
                    print(data)
                    print(type(data))
                    product_description["product_link"]=data["short_url"]
                    break
            if product_description["product_link"]!="":
                response["recommendations"].append(product_description)
        except Exception as e:
            print(e)
            print("Outer except")
            pass

    # get_product_details(product_description["product_link"],driver)
    driver.close()
    print(response)
    formatted_response="Based on the interaction, I would recommend you following: \n"
    print(formatted_response)
    for item in response["recommendations"]:
        print(item)
        if 'product_link' in item and 'product_name' in item:
            item_descp= f"""{item['product_name']} \n Link: {item["product_link"]} \n\n"""
            formatted_response=formatted_response+item_descp

    return formatted_response


@app.post("/whatsapp-bot")
def messaging(Body: str = Form()):
    try:
        message = Body.lower()
        print(message)
        message_split=message.split(" ")
        print(message_split)
        empty_field=find_empty_user_details_field()
        global user_details
        if len(message_split)==2 and message_split[0]=="phone" and message_split[1].isnumeric():
            global user_phone
            user_phone=message_split[1]
            return send_message(f"""Welcome to ShopAI. I am a AI Assisstant and I will help you to find best outfit from flipkart ph no. +91{user_phone}. Let's start with normal questionarrie: \n\n What's your age ?""")
        elif message=="clear":
            clear()
            return send_message("New Session Started: I am ready to answer your questions. plz tell your phonenumber as: Phone 98XXXXXXX")
        elif empty_field!='':
            user_details[empty_field]=message
            new_empty_field = find_empty_user_details_field()
            if new_empty_field!='':
                return send_message(empty_field_response[new_empty_field])
            else:
                return send_message("I am ready to take your queries. Plz tell what kind of outfit you want ?")
        user_details["userQuery"]=message
        scraped_response = scrape_flipkart_whatsapp(age=user_details["age"],location=user_details["location"],gender=user_details["gender"],curr_date=user_details["date"],user_instructions=user_details["user_instructions"],userQuery=user_details["userQuery"])
        print(scraped_response)
        return send_message(scraped_response)
    except Exception as e:
        print(e)
        return send_message("Give all inputs correctly")
    
@app.get("/trends")
def get_trends():
    global fashion_trends
    trend_messages=[{
        'role' : 'system',
        'content' : f'''you work for a fashion company and your task is to read from an array of strings in which each string is desciption of an image of a fashion influencer\n
        and your task is to understand about what new types of clothes they are wearing and what fashion trends is being followed.you are given this array = < {fashion_trends} >. \n
        take time to think & analyze while iterating through this array to understand what people are wearing and what is or can be name of those fashion clothes and what trends are these. you only speak JSON and output should strictly be like \n
        {{"fashion_trends" : ["array items should be name of fashion clothes currently trending after your analysis of this array.]}} \n
        and there should not be any extra text in your response'''
    }]
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", messages=trend_messages)
    print(chat_completion)
    gpt_response = json.loads(chat_completion['choices'][0]['message']['content'])
    return gpt_response