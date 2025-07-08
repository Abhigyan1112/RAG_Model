
import requests
from flask import Flask, request, jsonify, render_template, url_for, redirect
import fitz
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
import numpy as np
import json
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key = 'aditi18'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///RAG.db'
db=SQLAlchemy(app)

class FILE(db.Model):
    sno = db.Column(db.Integer,primary_key=True,autoincrement=True)
    file = db.Column(db.LargeBinary,nullable=False)

    def __repr__(self) -> str:
        return f'{self.sno}'

@app.route("/")
def main():
    full_response=request.args.get("full_response")
    return render_template('index.html',response=full_response or "")


@app.route("/Answer", methods=['POST'])
def answer():
    print("FILES RECEIVED:", request.files)
    file = request.files['file']
    query= request.form['query']
    filename=file.filename
    file=file.read()
    
    if not filename=='':
        db.session.query(FILE).delete()
        db.session.commit()
        entry=FILE(file=file)
        print("File is given")
        db.session.add(entry)
        db.session.commit()
    else:
        print("file is not given")
        file=db.session.query(FILE.file).distinct().all()
        file=file[0][0]

    file_stream=BytesIO(file)
    chunks = extract_chunks_from_pdf(file_stream)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    client=chromadb.Client()
    try:
        client.delete_collection(name="abcd")
    except Exception as e:
        print(f"Collection delete failed or does not exist: {e}")
    collection = client.get_or_create_collection(name="abcd") #Collection is like a vector table for the document

    try:
        collection.add(
            documents=chunks,
            ids=[f"chunk {i+1}" for i in range(len(chunks))],
            embeddings=model.encode(chunks)
        )
    except Exception as e:
        print(e)

    query_embedding=model.encode([query])[0]
    results=collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    relevant_chunks = results['documents'][0]
    context = "\n".join(relevant_chunks)

    url='https://api.groq.com/openai/v1/chat/completions'

    headers={
        "Content-Type":"application/json",
        "Authorization":f"Bearer {api_key}"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages":[
            {"role":"system","content":f"Context:{context}"},
            {"role":"user","content":query}
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    full_response=""
    if response.status_code == 200:
        full_response=response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Failed to generate response: {response.status_code}")
        print("Response text:", response.text)

    # full_response=full_response.strip()
    return redirect(url_for('main',full_response=full_response))



def extract_chunks_from_pdf(file,chunk_size=500):
    doc=fitz.open(stream=file,filetype='pdf')
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
    app.run(host="0.0.0.0",debug=True,port=8000)

