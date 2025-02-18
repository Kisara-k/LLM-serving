from openai import OpenAI
import requests
import os
load_dotenv()

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
RUNPOD_ENDPOINT_ID = 'qp5qwuo9s34ubx'
MODEL_NAME = 'mergekit-community/Deepseek-R1-Distill-NSFW-RPv1'

# RUNPOD_ENDPOINT_ID = 'n4yl6ilbb3q5zy'
# MODEL_NAME = 'meta-llama/Llama-3.1-8B'


client = OpenAI(
    api_key = RUNPOD_API_KEY,
    base_url = f'https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/openai/v1'
)

import threading

prompts = [
    "Describe discovering a hidden door in an ancient library.",
    "Tell a story about a lost civilization deep in the ocean.",
    "What happens when a scientist accidentally opens a portal to another dimension?",
    "Explain how an astronaut feels during their first spacewalk.",
    "Describe the moment a detective solves a decade-old mystery."
    "Describe discovering a hidden door in an ancient library.",
    "Tell a story about a lost civilization deep in the ocean.",
    "What happens when a scientist accidentally opens a portal to another dimension?",
    "Explain how an astronaut feels during their first spacewalk.",
    "Describe the moment a detective solves a decade-old mystery."
    # "Describe discovering a hidden door in an ancient library.",
    # "Tell a story about a lost civilization deep in the ocean.",
    # "What happens when a scientist accidentally opens a portal to another dimension?",
    # "Explain how an astronaut feels during their first spacewalk.",
    # "Describe the moment a detective solves a decade-old mystery."
    # "Describe discovering a hidden door in an ancient library.",
    # "Tell a story about a lost civilization deep in the ocean.",
    # "What happens when a scientist accidentally opens a portal to another dimension?",
    # "Explain how an astronaut feels during their first spacewalk.",
    # "Describe the moment a detective solves a decade-old mystery."
]

# Function to send a request and stream the response
def get_response(prompt, thread_id):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        top_p=1.0,
        n=1,
        max_tokens=5000,
        stop=["\n\n", "User:", "user:", "Assistant:", "I'm sorry"],
        stream=True,
        presence_penalty=0.0,
        frequency_penalty=0.0,
    )

    result = ""

    print(f"\n[Thread {thread_id}] Response for prompt: {prompt}\n")
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(f'{thread_id} ({content})', end=" ", flush=True)
            result += content
    print("\n[Thread {}] done".format(thread_id))
    print(result, '\n')

# Create and start multiple threads
threads = []
for i, prompt in enumerate(prompts):
    thread = threading.Thread(target=get_response, args=(prompt, i + 1))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("\nAll threads completed.")