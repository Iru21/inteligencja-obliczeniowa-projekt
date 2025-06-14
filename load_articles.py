import os
from stem_text import stem_text

def load_articles():
    saved_file = 'processed_articles.pkl'

    import pandas as pd
    if os.path.exists(saved_file):
        print(f"\nLoading pre-processed articles from {saved_file}...")
        return pd.read_pickle(saved_file)

    from tqdm import tqdm
    tqdm.pandas()
    # https://www.kaggle.com/datasets/aryansingh0909/nyt-articles-21m-2000-present
    df = pd.read_csv('articles.csv',
                     usecols=['abstract', 'lead_paragraph', 'pub_date'],
                     dtype={
                         'abstract': str,
                         'lead_paragraph': str,
                         'pub_date': str
                     })

    print(f'\nCleaning and filtering {df.shape[0]} articles...')
    df = df[df['abstract'].notnull() & (df['abstract'] != 'To the Editor:')]
    df = df[df['lead_paragraph'].notnull() & (df['lead_paragraph'] != 'To the Editor:')]
    df['pub_date'] = pd.to_datetime(df['pub_date'], errors='coerce')
    df['text'] = df['abstract'] + ' ' + df['lead_paragraph']
    df = df.drop(columns=['abstract', 'lead_paragraph'])
    df = df[df['text'].str.strip() != '']

    print("\nStemming article text...")
    df['text'] = df['text'].progress_apply(stem_text)

    print(f"\nSaving processed articles to {saved_file}...")
    df.to_pickle(saved_file)

    return df
