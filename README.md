# Article Sentiment Analysis

This application allows you to analyze the sentiment of news articles about a specific subject and generate word clouds from the article text.

## Features

- Search for articles by subject
- Analyze sentiment of articles over time (yearly and monthly)
- Generate word clouds from an article's text

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Download [articles.csv](ttps://www.kaggle.com/datasets/aryansingh0909/nyt-articles-21m-2000-present) into folder sources
4. Download nltk punkt_tab:
   ```
   python -m nltk.downloader punkt_tab
   ```

## Usage

1. Start the Flask server:
   ```
   python server.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Enter a subject in the input field (e.g., "Climate Change", "Artificial Intelligence")

4. Click "Analyze Sentiment" to generate sentiment analysis charts or "Generate Word Cloud" to create a word cloud

5. View the results in the web interface

## Running Scripts Directly

You can also run the Python scripts directly from the command line:

### Sentiment Analysis

```
python analyze_sentiment.py --subject "Climate Change"
```

### Word Cloud Generation

```
python cloud.py --subject "Climate Change"
```

## Output Files

- Sentiment charts are saved in the `sentiments` directory
- Word clouds are saved in the `wordclouds` directory

## Project Structure

- `index.html` - Web interface
- `script.js` - Frontend JavaScript
- `server.py` - Flask server
- `analyze_sentiment.py` - Sentiment analysis script
- `cloud.py` - Word cloud generation script
- `load_articles.py` - Article loading utility
- `stem_text.py` - Text stemming utility