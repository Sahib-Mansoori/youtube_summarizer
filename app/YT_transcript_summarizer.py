import time

import requests
import json
from YT_transcript_file_reader import read_file
import env

prompt = f"""
You are a professional content summarizer under 4000 characters. 
Given a transcript from a YouTube video, your task is to create a clear, concise summary in **English only**, formatted for Telegram messages (MarkdownV2).

{env.prompt}

Output should be ready to send directly as a Telegram message in MarkdownV2.
"""

auth = env.auth

llm_models = {"non_thinking":
                  env.non_thinking_models,

              "thinking":
                  env.thinking_models
              }


def call_model(model_name, transcript_content, file_name):
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}. Here is the youtube video name {file_name} and the transcript to process: '''{transcript_content}'''"
            }
        ]
    }

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": auth,
                "Content-Type": "application/json",
            },
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        elif response.status_code in [400, 401, 402]:
            return f"Issue with API call failed with status {response.status_code}: {response.text}"
        else:
            print(f"Model {model_name} failed with status {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"Model {model_name} raised an exception: {e}")
        return None


def summarize_transcript_with_llm(file_name):
    print(f"\nSummarizing the content for:\n{file_name}")
    transcript_content = read_file(file_name)
    if not transcript_content:
        return "No transcript found."

    for model_type in ['non_thinking', 'thinking']:
        for model_name in llm_models[model_type]:
            print(f"Trying model: {model_name}")
            summary = call_model(model_name, transcript_content, file_name)
            # If this summary length is more or equal to 1000 character
            if summary and len(summary) >= 1000:
                print(f"Success with model: {model_name}")
                summary_file_name = file_name.replace('.txt', '_summary.txt')
                write_to_file(summary_file_name, summary)
                return summary

    return "All models failed to generate summary."

def write_to_file(file_name, content):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)


def main():
    start = time.time()
    file = "transcript_Nothing Phone 3 Review_ They Lied!.txt"
    summary = summarize_transcript_with_llm(file)
    print(summary)
    print('Total time taken: ', time.time() - start)


if __name__ == '__main__':
    main()
