import argparse

parser = argparse.ArgumentParser(description='Analyze sentiment of articles about a specific subject')
parser.add_argument('--subject', type=str, default='Global Warming', help='Subject to analyze sentiment for')
args = parser.parse_args()
SUBJECT = args.subject

if SUBJECT == '':
    print("No subject specified. Please provide a subject using the --subject parameter.")
    exit()

print("\nLoading sentiment analysis model...")
from transformers import pipeline
sentiment_pipeline = pipeline("sentiment-analysis")
def analyze_sentiment(text):
    result = sentiment_pipeline(text[:512])[0]
    score = result['score']
    return score if result['label'] == 'POSITIVE' else -score

print("\nLoading articles...")
from load_articles import load_articles
df = load_articles()

print(f'\nSearching for articles mentioning "{SUBJECT}"...')
from stem_text import stem_text
stemmed_subject = stem_text(SUBJECT)
df = df[df['text'].str.contains(stemmed_subject, case=False, na=False)]
if df.empty:
    print(f"No articles found mentioning '{SUBJECT}'.")
    exit()

print(f"\nAnalyzing sentiment for {df.shape[0]} articles...")
df['sentiment'] = df['text'].progress_apply(analyze_sentiment)
df['year'] = df['pub_date'].dt.year
df['month'] = df['year'].astype(str) + '-' + df['pub_date'].dt.month.astype(str).str.zfill(2)

def calculate_average_sentiment(timescale):
    if timescale not in ['year', 'month']:
        raise ValueError("timescale must be either 'year' or 'month'")
    print(f'\nCalculating average sentiment by {timescale}...')
    average_sentiment = df.groupby(timescale)['sentiment'].mean().reset_index()

    import matplotlib.pyplot as plt
    if timescale == 'year':
        plt.figure(figsize=(10, 5))
    else:
        plt.figure(figsize=(60, 5))
    plt.plot(average_sentiment[timescale], average_sentiment['sentiment'], marker='o')
    plt.title(f'Average sentiment over {timescale}s for {SUBJECT} in {df.shape[0]} articles')
    plt.xlabel(f'{timescale.capitalize()}')
    plt.ylabel('Average Sentiment Score')
    plt.xticks(average_sentiment[timescale], rotation=45)
    plt.grid()
    plt.tight_layout()
    output_filename = f'sentiments/{SUBJECT.lower().replace(" ", "-")}-{timescale}s.png'
    plt.savefig(output_filename)
    print(f"Saved {timescale} sentiment chart to {output_filename}")
    # plt.show() - Commented out to prevent blocking when run from server

calculate_average_sentiment('year')
calculate_average_sentiment('month')
