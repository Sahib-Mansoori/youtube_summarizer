import time
import requests
import env

CHAT_ID = env.CHAT_ID   # Replace with your group chat ID
MESSAGE = "Hello, group! 🚀"
KEY = env.KEY

def escape_markdown_v2(text: str, aggressive: bool = False) -> str:
    """
    Escape characters for Telegram MarkdownV2.

    If aggressive=True, escape ALL asterisks instead of allowing bold/italic.
    """
    # Full list of MarkdownV2 special characters
    escape_chars = r'_*[]()~`>#+-=|{}.!'

    for ch in escape_chars:
        if aggressive and ch == "*":
            # escape * always (prevents bold/italic usage)
            text = text.replace(ch, f'\\{ch}')
        else:
            text = text.replace(ch, f'\\{ch}')
    return text


def send_telegram_message_split(message, max_retries=3, delay=2):
    """
    Send long messages to Telegram in chunks of <= 4096 chars.
    Handles retries, MarkdownV2 escaping, and fallback on bold errors.
    """
    message = message.replace("<br>", "\n")  # replace HTML breaks with newlines
    url = f"https://api.telegram.org/bot{KEY}/sendMessage"
    limit = 4096  # Telegram message length limit

    responses = []
    for i in range(0, len(message), limit):
        chunk = message[i:i + limit]
        chunk_v2_intact = escape_markdown_v2_intact(chunk)  # first-pass safe escaping

        payload = {
            "chat_id": CHAT_ID,
            "text": chunk_v2_intact,
            "parse_mode": "MarkdownV2"
        }

        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(url, data=payload, timeout=10)
                data = response.json()

                # If Telegram complains about bold/italic entity parsing
                if not data.get("ok") and "can't parse entities" in data.get("description", "").lower():
                    print(f"[Attempt {attempt}] Markdown issue detected: {data['description']}")
                    # Re-escape aggressively (escape all `*`) and retry once immediately
                    # safe_chunk = escape_markdown_v2(chunk, aggressive=True)
                    # safe_chunk = escape_markdown_v2_lost(chunk)
                    payload["parse_mode"] = "HTML"
                    payload["text"] = chunk
                    response = requests.post(url, data=payload, timeout=10)
                    data = response.json()

                print(data)
                responses.append(data)
                break  # success, break retry loop

            except requests.exceptions.RequestException as e:
                print(f"[Attempt {attempt}] Error sending chunk: {e}")
                if attempt < max_retries:
                    time.sleep(delay * attempt)  # exponential-ish backoff
                else:
                    responses.append({"ok": False, "error": str(e)})

    return responses

def escape_markdown_v2_intact(text: str) -> str:
    escape_chars = ['_', '**', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']


    for ch in escape_chars:
        if ch == '**':
            text = text.replace(ch, "*")
        text = text.replace(ch, f'\\{ch}')

    return text

def escape_markdown_v2_lost(text: str) -> str:
    escape_chars = ['_', '*', '**', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']


    for ch in escape_chars:
        # if ch == '*':
        #     text = text.replace(ch, "*")
        text = text.replace(ch, f'\\{ch}')

    return text

test_message = """
**Video Name:** “Don’t buy a Sony Camera until you watch this! 2025”

- **Focus of the video:**  
  *Overview of Sony camera lineup at the start of 2025, buying advice, and rumors about upcoming models.*  
  *Presenter is a camera‑review channel that often covers Sony gear, interrupted by sponsor plugs.*

- **Key Takeaways by Sensor Size**

  | Sensor | Main Models Discussed | Highlights & Buying Advice |
  |--------|-----------------------|-----------------------------|
  | **1‑inch (pocket)** | **RX100 series** (M5,M7,M8) & **ZV‑1** | - RX100 M5 discontinued; RX100 M7 still good if found under $1,100. <br>- ZV‑1 Mark 1 (24‑70/f1.8‑2.8) and Mark 2 (18‑50/f1.8‑4.0): Mark 2 offers improved UI; budget‑friendly fans can slot Mark 1. |
  | **1‑inch (cinema)** | **ZV‑E10 II**, **FX30** | - ZV‑E10 II is a budget cinema‑style body (no IBIS, no mechanical shutter). <br>- FX30 offers true 24 fps and full‑frame video; good under‑$2k. |
  | **APS‑C** | **A6700**, **A7000** (aka A6/A6900), **A7 R V** (rumored baby A9) | - A6700: best hybrid APS‑C for $1,400. <br>- A7000 (A6/A6900) popular but unlikely to drop below $2k; used A9 I or A9 II are cheaper alternatives. |
  | **Full‑frame** | **ZV‑E1**, **A75** (rumored), **A7 R VI**, **A7 S IV**, **A7C II/ R**, **RX1R III** | - ZV‑E1 is a cost‑effective full‑frame video body but overheats above 20 min 4K. <br>- A75 rumors: 4K 60p & 120 fps full‑frame, no crop, higher IS, 8‑stop IBIS (release uncertain, 2025‑2026). <br>- A7 R VI: expect 60‑80 MP, better cropped‑zoom UI. <br>- A7 S IV: likely vanishing; FX3 Mark II may replace it. <br>- A7C II/ R: solid compact, 4K 60p, expect price cuts end‑2024. <br>- RX1R III: future premium fixed‑lens full‑frame, may sit above A7C in price. |
  | **Flagship** | **A9 II**, **A1** | - A9 II: 24 MP, 120 fps, global shutter. <br>- A1: 50 MP, 30 fps, no global shutter (still a powerhouse). <br>- Both have “pre‑capture” mode for high‑speed photography. <br>- No expected updates until 2027; older models drop in used market. |

- **General Buying Advice**  
  * Hold off on newer releases if you can secure a discounted or second‑hand unit of a recent pre‑release.  
  * For pure video, the FX3/FX3‑Mark II or ZV‑E1 (budget) are solid, but expect firmware updates for better stabilization and AI tracking.  
  * For hybrid shooters, the A6700 remains the best value, while A7 R VI offers higher resolution when needed.

- **Other Mentions**  
  * AF‑friendly “in‑camera crop” UI improvements would help high‑pixel models (A7 R VI).  
  * Expect price cuts on A7C, FX30, and FX3 models toward year‑end.  
  * Sponsor plug: Squarespace website builder.

- **Conclusion**  
  The channel presents a comprehensive walk‑through of Sony’s current lineup, telling viewers which cameras still hold up, when to expect updates, and how to snag a good deal. The video directs viewers to buy wisely in 2025, especially avoiding the newest releases until they’re offers or depreciated.

"""

def main():
    send_telegram_message_split(test_message, max_retries=5, delay=5)

if __name__ == '__main__':
    main()
