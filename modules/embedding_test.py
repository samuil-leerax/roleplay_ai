from openai import OpenAI
import os
import keys
import temp_modules.testdata as testdata

import numpy as np

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

api_key = keys.api_key

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

def embed(text):
    response =  client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return(response.data[0].embedding)

dat = []
for i in testdata.memory:
    memory_dat = i["memory"]
    embeding_ = embed(memory_dat)
    output_data = {"vector": embeding_, "content": memory_dat}
    dat.append(output_data)

prompt = embed("""

Кого ты сегодня впускал к себе домой?

""")

min_to_use = 0.3

for i in dat:
    siml = cosine_similarity(prompt, i["vector"])
    if(siml >= min_to_use):
        print(i["content"] + "\n------------\n")




