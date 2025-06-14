SUBJECT = 'Climate Change'

print("Loading sentiment analysis model...")
from transformers import pipeline
sentiment_pipeline = pipeline("sentiment-analysis")
def analyze_sentiment(text):
    result = sentiment_pipeline(text[:512])[0]
    score = result['score']
    return score if result['label'] == 'POSITIVE' else -score

print("Loading articles...")
from load_articles import load_articles
df = load_articles()

print("Stemming article text...")
from stem_text import stem_text
df['text'] = df['text'].progress_apply(stem_text)

print(f'Searching for articles mentioning "{SUBJECT}"...')
stemmed_subject = stem_text(SUBJECT)
df = df[df['text'].str.contains(stemmed_subject, case=False, na=False)]

print(f"Analyzing sentiment for {df.shape[0]} articles...")
df['sentiment'] = df['text'].progress_apply(analyze_sentiment)
df['year'] = df['pub_date'].dt.year

print(f'Calculating average sentiment for each year...')
average_sentiment = df.groupby('year')['sentiment'].mean().reset_index()

print(f'Average sentiment calculated.')
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 5))
plt.plot(average_sentiment['year'], average_sentiment['sentiment'], marker='o')
plt.title(f'Average Sentiment Over Time for {SUBJECT} in {df.shape[0]} articles')
plt.xlabel('Year')
plt.ylabel('Average Sentiment Score')
plt.xticks(average_sentiment['year'], rotation=45)
plt.grid()
plt.tight_layout()
plt.savefig(f'sentiments/{SUBJECT.lower().replace(" ", "-")}.png')
plt.show()


