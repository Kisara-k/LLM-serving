from openai import OpenAI
import requests
import asyncio
import os
load_dotenv()

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
RUNPOD_ENDPOINT_ID = 'qp5qwuo9s34ubx'

client = OpenAI(
    api_key = RUNPOD_API_KEY,
    base_url = f'https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/openai/v1'
)

MODEL_NAME = 'mergekit-community/Deepseek-R1-Distill-NSFW-RPv1'

async def create_completion(prompt, client):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            top_p=1.0,
            n=1,
            max_tokens=5000,
            stop=["\n\n", "User:", "user:", "Assistant:", "I'm sorry"],
            stream=True,
            presence_penalty=0.0,
            frequency_penalty=0.0,
        )
        
        result = []
        loop = asyncio.get_running_loop()

        # Run the blocking generator in a separate thread to avoid blocking the event loop
        def fetch_stream():
            for chunk in response:
                content = chunk.choices[0].delta.get("content", "")
                if content:
                    result.append(content)

        await loop.run_in_executor(None, fetch_stream)

        print(f"\nPrompt: {prompt}\nResponse: {''.join(result)}\nDone.\n")
        return ''.join(result)

    except Exception as e:
        print(f"Error: {e}")
        return None

async def run_parallel_requests(prompts):
    tasks = [create_completion(prompt, client) for prompt in prompts]
    results = await asyncio.gather(*tasks)
    return results


if __name__ == "__main__":
    # List of prompts for parallel requests
    prompts = [
        "Describe discovering a hidden door in an ancient library.",
        "Explain how a black hole works.",
        "What are the benefits of meditation?",
        "How do quantum computers differ from classical computers?",
        "Write a short story about a talking tree.",
        "What is the history of the Silk Road?",
        "Describe the process of photosynthesis.",
        "Tell me about the Great Wall of China.",
        "How does blockchain technology work?",
        "What is the theory of relativity?"
    ]
    
    # Run parallel requests
    asyncio.run(run_parallel_requests(prompts))
