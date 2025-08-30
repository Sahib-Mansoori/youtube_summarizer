import time
from YT_telegram_message import send_telegram_message_split
from YT_transcript_multiple import get_youtube_transcript, get_urls
from YT_transcript_summarizer import summarize_transcript_with_llm
from YT_feed_with_tracking_with_limit import get_feed_urls, save_processed_link
import re


def summarize_youtube_videos(url_arg=None):
    """
    Fetch transcript(s) for one or more YouTube videos and generate summary/ies.

    - Accepts either a single URL (string) or a list of URLs.
    - Downloads transcripts and corresponding filenames.
    - Summarizes each transcript using an LLM summarizer.
    - Prepends the video URL to each summary for context.
    - Returns a list of summaries (one per video).
    """

    # Ensure a URL is provided, otherwise raise an error
    if not url_arg:
        raise ValueError("No valid URL provided.")

    # Normalize input: always work with a list of URLs
    urls = url_arg if isinstance(url_arg, list) else [url_arg]

    # Fetch transcripts and their corresponding filenames
    transcripts, filenames = get_youtube_transcript(urls)

    # If no transcripts were found, log and return an empty list
    if not transcripts:
        print("No transcript found to summarize")
        return []

    # Collect all generated summaries here
    summaries = []

    # Iterate through each transcript + filename pair
    for index, transcript in enumerate(transcripts):
        try:
            # Generate a summary for the current transcript
            # (currently using filename as input to the summarizer)
            filename = filenames[index]
            summary = summarize_transcript_with_llm(filename)

            # Prepend the video URL to the summary for context
            summary = add_url_in_summary(urls)+ add_video_name_in_summary(filename) + summary

            # Print summary to console with separators for debugging/inspection
            print('***' * 50)
            print(summary)
            print('***' * 50)

            # Store the summary in the results list
            summaries.append(summary)

        except Exception as e:
            # Catch and log any errors for this specific transcript
            print(f"Error summarizing {filenames[index]}: {e}")

    # Return the list of summaries (could be empty if all failed)
    return summaries



def add_url_in_summary(url):
    text = f"{url[0]}\n\n"
    return text

def add_video_name_in_summary(video_name: str):
    text = f"{video_name.removesuffix('.txt').removeprefix('transcript_')}\n\n"
    return text

def get_urls_or_feed():
    """
    Prompt the user for input:
    - If user enters 'feed', return None (indicating RSS mode).
    - Otherwise, treat input as manual YouTube URLs (comma-separated).
    - Only accepts valid YouTube video URLs. Any invalid input raises ValueError.
    """

    user_input = input("Enter YouTube video URLs (comma separated), or type 'feed' for RSS feed: ").strip()

    if not user_input:
        raise ValueError("No input provided.")

    # If 'feed', trigger RSS fetching
    if user_input.lower() == "feed":
        return get_feed_urls()

    # Regex to validate YouTube URLs (normal + short links)
    youtube_pattern = re.compile(
        r'^(https?://)?(www\.)?(youtube\.com/watch\?v=[\w\-]{11}|youtu\.be/[\w\-]{11})([&?]\S*)?$',
        re.IGNORECASE
    )

    urls = [url.strip() for url in user_input.split(",") if url.strip()]

    # Validate all URLs
    for url in urls:
        if not youtube_pattern.match(url):
            raise ValueError(f"Invalid YouTube URL provided: {url}")

    return urls

def check_all_responses(responses: list):
    ok_list = []
    for obj in responses:
        ok_status = (obj['ok'])
        ok_list.append(ok_status)
    if False in ok_list:
        return False
    else:
        return True



def main():
    start = time.time()

    # Get input from user
    urls = get_urls_or_feed()

    # If user typed "feed", fetch URLs from channel RSS
    if urls is None:
        urls = get_feed_urls()

    # Process each video URL
    for url in urls:
        try:
            summaries = summarize_youtube_videos(url)
            for summary in summaries:
                if summary:
                    responses = send_telegram_message_split(summary, max_retries=5, delay=2)
                    if check_all_responses(responses):
                        save_processed_link(url)  # Save only after success
        except Exception as e:
            print(f"Error processing {url}: {e}")

    print(f"Total time: {time.time() - start:.2f} seconds")


if __name__ == "__main__":
    main()
