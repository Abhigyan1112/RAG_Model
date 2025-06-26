{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "8c658d06-bb9f-4957-afd6-cedfe26de5b9",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Ollama Server URL:  https://3d51-2401-4900-1ca2-7458-2c7a-3a68-b955-aea2.ngrok-free.app\n"
     ]
    }
   ],
   "source": [
    "NGROK_TOKEN = \"2yluDrvHL5c9vDBng1gDfw719D6_yJGbtDGREbCLAvKizMW2\"\n",
    "\n",
    "from pyngrok import ngrok \n",
    "\n",
    "#Here we are exposing the Ollama server to the internet with the help of ngrok\n",
    "public_url=ngrok.connect(11434,\"http\",host_header=\"localhost:11434\").public_url\n",
    "print(\"Ollama Server URL: \",public_url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "249af274-be81-491d-9356-08176ca0a9c0",
   "metadata": {
    "jupyter": {
     "source_hidden": true
    }
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{\"models\":[{\"name\":\"mistral:latest\",\"model\":\"mistral:latest\",\"modified_at\":\"2025-06-20T17:42:48.0779874+05:30\",\"size\":4113301822,\"digest\":\"3944fe81ec14610e0852c3d915768ee8d507ea541387fdfcbbf9edaa0c757734\",\"details\":{\"parent_model\":\"\",\"format\":\"gguf\",\"family\":\"llama\",\"families\":[\"llama\"],\"parameter_size\":\"7.2B\",\"quantization_level\":\"Q4_0\"}}]}"
     ]
    }
   ],
   "source": [
    "#sending an HTTP get request to the server api tags\n",
    "!curl {public_url}/api/tags"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "a7efda90-0de5-4030-8031-b98792897223",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The public_url is successfully working\n"
     ]
    }
   ],
   "source": [
    "import requests\n",
    "try:\n",
    "    response=requests.get(public_url)\n",
    "    if response.status_code==200:\n",
    "        print(\"The public_url is successfully working\")\n",
    "    else:\n",
    "        print(\"Status Code:\",response.status_code)\n",
    "except Exception as e:\n",
    "    print(\"Error\",e)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "98db0d2b-89ca-4794-a8a3-b001ae2d3928",
   "metadata": {},
   "outputs": [],
   "source": [
    "pdf_path=\"William.pdf\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "id": "de93e1f6-4b54-4996-92c5-62dc5539ead9",
   "metadata": {},
   "outputs": [],
   "source": [
    "import fitz\n",
    "\n",
    "def extract_chunks_from_pdf(pdf_path,chunk_size=500):\n",
    "    doc=fitz.open(pdf_path)\n",
    "    all_text=' '\n",
    "    \n",
    "    for page in doc:\n",
    "        text=page.get_text()\n",
    "        clean_text=' '.join(text.split())\n",
    "        all_text+=clean_text+' '\n",
    "\n",
    "    doc.close()\n",
    "\n",
    "    words=all_text.split()\n",
    "    chunks=[' '.join(words[i:i+chunk_size]) for i in range(0,len(words),chunk_size)]\n",
    "\n",
    "    return chunks"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 51,
   "id": "1118faef-c2ed-43ff-8676-10bbfc205266",
   "metadata": {},
   "outputs": [],
   "source": [
    "from sentence_transformers import SentenceTransformer\n",
    "import chromadb\n",
    "from chromadb.utils import embedding_functions\n",
    "import numpy as np\n",
    "\n",
    "model = SentenceTransformer(\"all-MiniLM-L6-v2\")\n",
    "client=chromadb.Client()\n",
    "collection = client.create_collection(name=\"William_doc\",get_or_create=True) #Collection is like a vector table for the document\n",
    "\n",
    "def build_chromadb_index(chunks):\n",
    "    collection.add(\n",
    "        documents=chunks,\n",
    "        ids=[f\"chunk {i+1}\" for i in range(len(chunks))],\n",
    "        embeddings=model.encode(chunks)\n",
    "    )\n",
    "\n",
    "def get_relevant_chunks(query):\n",
    "    query_embedding=model.encode([query])[0]\n",
    "    results=collection.query(\n",
    "        query_embeddings=[query_embedding], \n",
    "        n_results=3\n",
    "    )\n",
    "    return results"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 69,
   "id": "38d1b38c-fcfa-40f7-9cde-eee181cd6b43",
   "metadata": {},
   "outputs": [],
   "source": [
    "import requests\n",
    "import json\n",
    "\n",
    "def generate_response(query,context):\n",
    "    url=f'{public_url}/api/generate'\n",
    "    headers={\"Context-Type\":\"application/json\"}\n",
    "    data={\"model\":\"mistral\",\n",
    "          \"prompt\":f\"Context:{context}\\n\\n Question:{query}\\n Answer:\"}\n",
    "\n",
    "    response = requests.post(url, json=data, headers=headers, stream=True)\n",
    "    full_response=\"\"\n",
    "    if response.status_code == 200:\n",
    "        for line in response.iter_lines():\n",
    "            if line:\n",
    "                try:\n",
    "                    decoded_line = line.decode(\"utf-8\")\n",
    "                    json_obj = json.loads(decoded_line)\n",
    "                    full_response += json_obj.get(\"response\", \"\")\n",
    "                except json.JSONDecodeError:\n",
    "                    continue\n",
    "        return full_response.strip()\n",
    "    else:\n",
    "        raise Exception(f\"Failed to generate response: {response.text}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 70,
   "id": "5422e77e-0b07-4b0a-bfb2-dab63ca1739e",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Yes, it's obvious that William is the main character in this context. He is the one experiencing events and undergoing significant emotional turmoil, which are key characteristics of a protagonist. Despite his struggles and conflicted emotions, his actions and feelings are central to the narrative, making him a protagonist rather than an antagonist.\n"
     ]
    }
   ],
   "source": [
    "query=\"Is it obvious that William is the main character. Is he a protagonist or an antagoist\"\n",
    "relevant_chunks=get_relevant_chunks(query)['documents'][0]\n",
    "context='/n'.join(relevant_chunks)\n",
    "print(generate_response(query,context))"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (RAGModel)",
   "language": "python",
   "name": "ragmodel"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
