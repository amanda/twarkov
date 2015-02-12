# twarkov
Markov text-generator for Twitter timelines. Deals with @ mentions, hashtags, and URLs.

## installation
With pip:
```pip install twarkov```

## example usage
See ```example.py```. You'll need Twitter API credentials to scrape a timeline, and to set them as environment variables for the example script to work. First replace the '???' below with your creds and run these commands in your terminal:

```
export APP_KEY='???'
export APP_SECRET='???'
export OAUTH_TOKEN='???'
export OAUTH_TOKEN_SECRET='???'
```

Then clone this repo, create a virtualenv, and install requirements:
```
git clone https://github.com/amandapickering/twarkov.git
mkvirtualenv twarkov
pip install -r requirements.txt
```

Edit ```example.py``` to add your twitter handle, then run it:
```python example.py```

You'll see a markov-generated tweet each time you run the script.

you can also tweak the ngram–```example.py``` uses 1 for more randomness, 2 (the default) works as well.

## todo
- still some issues with apostrophes in the middle of words
- no conjunctions at the end of a tweet
