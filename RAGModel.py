#!/usr/bin/env python
# coding: utf-8

from pyngrok import ngrok
import requests
from flask import Flask, request, jsonify, render_template, flash
import fitz
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
import numpy as np
import json

#Here we are exposing the Ollama server to the internet with the help of ngrok
public_url=ngrok.connect(11434,"http",host_header="localhost:11434").public_url
print(public_url)
# public_url="http://localhost:11434"

app=Flask(__name__)
@app.route("/")
def main():
    #sending an HTTP get request to the server api tags
    response=requests.get(public_url+'/api/tags')
    try:
        if response.status_code==200:
                print("The public_url is successfully working")
        else:
            print("Status Code:",response.status_code)
    except Exception as e:
        print("Error",e)
    return render_template('index.html')


@app.route("/Answer", methods=['POST'])
def answer():
    print("FILES RECEIVED:", request.files)
    file = request.files['file']
    query= request.form['query']

    model = SentenceTransformer("all-MiniLM-L6-v2")
    client=chromadb.Client()
    collection = client.create_collection(name=file.name,get_or_create=True) #Collection is like a vector table for the document
    file_path = f"static/files/{file.filename}"
    file.save(file_path)
    chunks = extract_chunks_from_pdf(file_path)

    collection.add(
        documents=chunks,
        ids=[f"chunk {i+1}" for i in range(len(chunks))],
        embeddings=model.encode(chunks)
    )

    query_embedding=model.encode([query])[0]
    results=collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    relevant_chunks = results['documents'][0]
    context = "\n".join(relevant_chunks)

    url=f'{public_url}/api/generate'
    headers={"Content-Type":"application/json"}
    data={"model":"mistral",
        "prompt":f"Context:{context}\n\n Question:{query}\n Answer:"}

    response = requests.post(url, json=data, headers=headers, stream=True)
    full_response=""
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                try:
                    decoded_line = line.decode("utf-8")
                    json_obj = json.loads(decoded_line)
                    full_response += json_obj.get("response", "")
                except json.JSONDecodeError:
                    continue
    else:
        raise Exception(f"Failed to generate response: {response.status_code}")

    full_response=full_response.strip()
    print(full_response)
    return render_template('index.html',response=full_response)



def extract_chunks_from_pdf(pdf_path,chunk_size=500):
    doc=fitz.open(pdf_path)
    all_text=' '

    for page in doc:
        text=page.get_text()
        clean_text=' '.join(text.split())
        all_text+=clean_text+' '

    doc.close()

    words=all_text.split()
    chunks=[' '.join(words[i:i+chunk_size]) for i in range(0,len(words),chunk_size)]

    return chunks


if __name__ == "__main__":
    app.run(debug=True,port=8000)

