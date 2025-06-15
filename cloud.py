SUBJECT = 'Climate Change'

print("\nLoading articles...")
from load_articles import load_articles
df = load_articles(stem=False)

if SUBJECT != '':
    print(f'\nSearching for articles mentioning "{SUBJECT}"...')
    df = df[df['text'].str.contains(SUBJECT, case=False, na=False)]
    if df.empty:
        print(f"No articles found mentioning '{SUBJECT}'.")
        exit()

print(f"\nProcessing article {df.shape[0]} articles...")
all_text = ' '.join(df['text'].tolist())

print(f"\nGenerating word cloud from article text ({len(all_text.split())} words)...")
from wordcloud import WordCloud
wordcloud = WordCloud(
    width=1200, 
    height=800,
    background_color='white',
    max_words=200,
    contour_width=3,
    contour_color='steelblue'
).generate(all_text)

import matplotlib.pyplot as plt
plt.figure(figsize=(16, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title(f'Word Cloud from {df.shape[0]} NYT Articles')
plt.tight_layout()

import os
os.makedirs('wordclouds', exist_ok=True)
output_path = 'wordclouds/articles_wordcloud.png' if SUBJECT == '' \
                else f'wordclouds/{SUBJECT.lower().replace(" ", "_")}_wordcloud.png'
plt.savefig(output_path)
print(f"\nWord cloud saved to {output_path}")
plt.show()
