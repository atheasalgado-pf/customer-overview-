import json
import os

# Keywords for sentiment classification
POSITIVE = ["thanks", "great", "excellent", "excited", "solved", "resolved", "confirmed", "working", "approved"]
NEGATIVE = ["issue", "problem", "blocked", "error", "failing", "frustrated", "delay", "missing", "urgent", "help"]

def analyze_sentiment(text):
    text = text.lower()
    pos_score = sum(1 for word in POSITIVE if word in text)
    neg_score = sum(1 for word in NEGATIVE if word in text)
    
    if neg_score > pos_score:
        return "Concerned"
    elif pos_score > neg_score:
        return "Positive"
    else:
        return "Neutral"

def main():
    try:
        with open('processed_summary.json', 'r') as f:
            narratives = json.load(f)
    except Exception as e:
        print(f"Error reading narratives: {e}")
        return

    sentiment_results = {}
    for tc, data in narratives.items():
        narrative = data.get('narrative', '')
        sentiment_results[tc] = analyze_sentiment(narrative)
    
    with open('sentiment_data.json', 'w') as f:
        json.dump(sentiment_results, f, indent=4)
    
    print(f"Analyzed sentiment for {len(sentiment_results)} customers.")

if __name__ == "__main__":
    main()
