
import os
from datetime import datetime
from zoneinfo import ZoneInfo

def main():
    now = datetime.now(ZoneInfo("America/New_York"))
    print("Weston Life Daily News")
    print("Boston time:", now.isoformat())

    required = ["OPENAI_API_KEY", "NEWS_API_KEY"]
    missing = [key for key in required if not os.getenv(key)]

    if missing:
        print("News publishing skipped.")
        print("Missing configuration:", ", ".join(missing))
        return

    print("API credentials detected.")
    print("Publishing paused until source verification and")
    print("archiving modules are configured.")

if __name__ == "__main__":
    main()
  
