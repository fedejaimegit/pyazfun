import azure.functions as func
import datetime
import json
import logging
import csv
import codecs
from blueprint import blueprint
import base64
import io
from PyPDF2 import PdfReader, PdfWriter
#from PyPDF2.generic import TextStringObject
#from PyPDF2.generic import DictionaryObject, NameObject, BooleanObject, ArrayObject
#from collections import defaultdict


app = func.FunctionApp()

app.register_functions(blueprint) 

@app.function_name('FirstHTTPFunction')
@app.route(route="myroute", auth_level=func.AuthLevel.ANONYMOUS)
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(
        "Wow this first HTTP Function works!!!!",
        status_code=200
    )

@app.function_name('SecondHTTPFunction')
@app.route(route="newroute")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting the second HTTP Function request.')
    
    name = req.params.get('name')
    if name:
        message = f"Hello, {name}, so glad this Function worked!!"
    else:
        message = "Hello, so glad this Function worked!!"
    return func.HttpResponse(
        message,
        status_code=200
    )


@app.function_name(name="MyFirstBlobFunction")
@app.blob_trigger(arg_name="myblob", 
                  path="blob-fede/People.csv",
                  connection="AzureWebJobsStorage")
def test_function(myblob: func.InputStream):
   logging.info(f"Python blob Function triggered after the People.csv file was uploaded to the newcontainer. So cool!!!! \n"
                f"Printing the name of the blob path: {myblob.name}"
                )
   

@app.function_name(name="ReadFileBlobFunction")
@app.blob_trigger(arg_name="readfile",
                  path="blob-fede/People2.csv",
                  connection="AzureWebJobsStorage")
def main(readfile: func.InputStream):
    reader=csv.reader(codecs.iterdecode(readfile,'utf-8'))
    for line in reader:
        print(line)

