def load_articles(stem=True):
    import os
    if not os.path.exists('sources/articles.csv'):
        os.makedirs('sources', exist_ok=True)
        raise FileNotFoundError("The articles.csv file is required but not found. "
                                "Please download it from the Kaggle dataset: "
                                "https://www.kaggle.com/datasets/aryansingh0909/nyt-articles-21m-2000-present" +
                                " and place it in the 'sources' directory.")

    saved_file = 'sources/processed_articles.pkl' if stem else 'sources/processed_articles_no_stem.pkl'

    import pandas as pd
    from tqdm import tqdm
    tqdm.pandas()
    if os.path.exists(saved_file):
        print(f"\nLoading pre-processed articles from {saved_file}...")
        return pd.read_pickle(saved_file)

    # https://www.kaggle.com/datasets/aryansingh0909/nyt-articles-21m-2000-present
    df = pd.read_csv('sources/articles.csv',
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

    if df.empty:
        print("No articles found. Please check the data source or parameters.")
        exit()

    if stem:
        print("\nStemming article text...")
        from stem_text import stem_text
        df['text'] = df['text'].progress_apply(stem_text)

    print(f"\nSaving processed articles to {saved_file}...")
    df.to_pickle(saved_file)

    return df
