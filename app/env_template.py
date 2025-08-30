# before beginning please remame this file from 'env_template.py' to 'env.py'

#  add channel ID of the YouTube channel for which you want to fetch the feed and get the summaries
# type(str) example = "UCx8Z14PpntdaxCt2hakbQLQ"
channel_id = "Your channel ID."

# add your openrouter API key here
# type(str)
auth = "your Openrouter api key"

# add your llm models from the openrouter
# non-thinking models
# type(list), example = ["mistralai/mistral-nemo:free", "mistralai/mistral-small-3.1-24b-instruct:free"]
non_thinking_models = ["mistralai/mistral-nemo:free",
                       "mistralai/mistral-small-3.1-24b-instruct:free"]

# thinking models
# type(list), example = ["mistralai/mistral-nemo:free", "mistralai/mistral-small-3.1-24b-instruct:free"]
thinking_models = ["deepseek/deepseek-r1:free",
                   "qwen/qwen3-235b-a22b:free"]

# telegram chat ID or channel ID where you want to send your message
# type(str)
CHAT_ID = "Your chat id"

# telegram bot API key that will send message to the chat or channel
# type(str)
KEY = "Your telegram bought API key."

# custom prompt that you want to give to summarize the summary (currently using a generic prompt)
# type(str)
prompt = """
Requirements:
- If the transcript contains non-English text (e.g., Hindi or mixed languages), translate it into clear English before summarizing.
- Summarize intelligently based on the type of video:
  • Educational/Tutorial → list key concepts, steps, or tips.
  • Podcast/Interview → mention the speakers, main discussion topics, and key takeaways.
  • News/Commentary → capture the main story, key facts, and conclusions.
  • Vlog/Informal → summarize events, highlights, or stories in a natural tone.
- Use simple bullet points or short paragraphs (no tables or complex formatting).
- Escape or avoid characters that break Telegram MarkdownV2 formatting.
- Avoid repeating filler words, irrelevant chatter, or overly long sentences.
- If the transcript is messy or incomplete, infer meaning and provide a useful summary anyway.
- Keep the style mobile-friendly: concise, scannable, and easy to read.
- **Final output must always be fully in English.**
"""
