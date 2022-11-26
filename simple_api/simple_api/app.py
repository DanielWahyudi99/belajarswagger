import pandas as pd
import numpy as np
import random
import regex as re
import sqlite3
import os
import io
import csv

from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

#string input tweet
def readdatacsvframe(input_tweet= None , csv_tweet = None):
    conn = sqlite3.connect('test_database2')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS products (Tweet text, price number)')
    conn.commit()
    c.execute('DELETE FROM products ')
    conn.commit()
    if input_tweet : 
        print ("input_tweetinput_tweetinput_tweetinput_tweet")
        print (input_tweet)
        c.execute('INSERT INTO products(Tweet) values ("%s") ' % input_tweet)
        conn.commit()

    if csv_tweet  :
        print ("asdfasdfsadffasdfsadfsdfasdfsadfasdfsadf") 
        print(csv_tweet)
        dfcsv_tweet = pd.read_csv(csv_tweet,encoding='latin-1') 
        dfcsv_tweet.to_sql('products' , conn, if_exists='replace', index = False)
        conn.commit()

    pd.set_option('display.max_rows', None)

    dfabbusive = pd.read_csv('abusive.csv')    

    dfss = pd.read_sql_query("SELECT * FROM products", conn)

    tweettolist3= list(set(dfss["Tweet"]))

    dfabbusive.to_sql('productsabbusive', conn, if_exists='replace', index = False)

    dfabbusive = pd.read_sql_query("SELECT * FROM productsabbusive", conn)

    abbusivetolist3= list(set(dfabbusive["ABUSIVE"]))

    tweettolistsetelahregex = []

    for i in tweettolist3:
        
        pattern = r",*(\s*\b(?:{}))\b".format("|".join(abbusivetolist3))
        hasildiregex= re.sub(pattern, "__SENSOR__", i) 
    
        tweettolistsetelahregex.append(hasildiregex)
        
    df2s = pd.DataFrame (tweettolistsetelahregex, columns = ['column_setelahdifilter'])
    df2s

    df2s.to_sql('hasilsetelahdicleaning', conn, if_exists='replace', index = False)

    c.execute('DELETE FROM products ')
    conn.commit()

    outputhasil = ""

    if input_tweet:
        print ("ini twetttt input biasa")
        outputhasil = df2s.values.tolist()[0][0]
    if csv_tweet :
        print ("ini csv tweet")
        outputhasil = df2s.values.tolist()    
    
    return outputhasil







app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'API Documentation for Data Processing and Modeling'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Dokumentasi API untuk Data Processing dan Modeling')
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json'
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,config=swagger_config)

@swag_from("docs/hello_world.yml", methods=['GET'])
@app.route('/', methods=['GET'])
def hello_world():

    resulthasil = readdatacsvframe("ampas")

    json_response = {
        'status_code': 200,
        'description': "Menyapa Hello World",
        'data': resulthasil
    }

   
    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text.yml", methods=['GET'])
@app.route('/text', methods=['GET'])
def text():
    json_response = {
        'status_code': 200,
        'description': "Original Teks",
        'data': "Halo, apa kabar semua?"
    }

    response_data = jsonify(json_response)
    return response_data


@swag_from("docs/text_clean.yml", methods=['GET'])
@app.route('/text-clean', methods=['GET'])
def text_clean():
    json_response = {
        'status_code': 200,
        'description': "Original Teks",
        'data': re.sub(r'[^a-zA-Z0-9]', ' ', "Halo, apa kabar semua?")
    }

    response_data = jsonify(json_response)
    return response_data


@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processingssss', methods=['POST'])
def text_processing():

    text = request.form.get('text')
    resulthasil = readdatacsvframe(text)

    json_response = {
        'status_code': 200,
        'description': "Original Teks",
        #'data': re.sub(r'[^a-zA-Z0-9]', '###', text)
        'data': resulthasil

       
    }

    response_data = jsonify(json_response)
    return response_data  


@swag_from("docs/text_fileupload.yml", methods=['POST'])
@app.route('/text-uploadfile', methods=['POST'])
def text_uploadfile():

    #fileoke = csv.reader(request.files['file'])
    # fileoke = csv.reader(request.files['file'])
    filesaveku = "data_uploaded.csv"
    request.files['file'].save(filesaveku) 

    #fileku = open(filesaveku)

    

    # dfssss = pd.DataFrame(csv.reader(request.files['file']))
    # csvfile =dfssss.to_csv('data_uploadedss.csv', sep='\t', encoding='utf-8')
    #dfssss  = pd.DataFrame({'A' : ['ampas', 1], 'B' : [1, 6]})
    #csvfile =dfssss.to_csv('data_uploadedss.csv', sep='\t', encoding='utf-8')

    #dfabbusivesss = pd.read_csv('abusive.csv')  
        
        #
        #import ipdb; ipdb.set_trace() 
    
    resultnya = readdatacsvframe(csv_tweet=filesaveku)

    
    json_response = {
        'status_code': 200,
        'description': "Original Teks",
        #'data': re.sub(r'[^a-zA-Z0-9]', '###', text)
        'data': resultnya

       
    }

    response_data = jsonify(json_response)
    return response_data  


if __name__ == '__main__':
    app.run()
