from datetime import datetime
import logging
import os
import re
import time
import urllib

import feedparser
import pandas as pd
import tqdm


logger = logging.getLogger(__name__)


def slow_load_feeds_df_from_url(feed_list_fn):
    """
    Loads rss urls one at a time.  Loads sequentially.

    This is totally unoptimized.


    :param str feed_list_fn: the path to a file containing a newline delimited
    list of urls of feeds.
    :return:
    """
    with open(feed_list_fn) as f:
        feed_urls = f.read().split()

    feeds = []
    for feed_url in feed_urls:
        try:
            feeds.append(feedparser.parse(feed_url))
        except Exception as e:
            logger.warning("An exception occurred during parsing of "
                           "{}, with message {}".format(feed_url, e.message))

    df = pd.DataFrame([
        {
            "author": feed["feed"]["author"],
            "feed_title": feed["feed"]["title"],
            "title": entry["title"],
            "href": link["href"],
            "length": link.get("length", 0),
            "type": link["type"],
            "date": datetime(*entry["published_parsed"][:6]).date(),
        }
        for feed in feeds
        for entry in feed["entries"]
        for link in entry["links"]
    ])
    return df


def normalize(x):
    return re.sub(r"[^a-z]+", " ", x.lower()).strip().replace(" ", "_")


def get_feed_df(fn="./feeds.csv"):
    feeds_df = pd.read_csv(fn, index_col=0)
    feeds_df["path"] = (
        "podcasts/"
        + feeds_df.author.apply(normalize)
        + "/"
        + feeds_df.title.apply(normalize)
        + "/"
        + feeds_df.date.apply(str)
        + "."
        + feeds_df.type.apply(lambda t: t.split("/")[1])
    )
    feeds_df["exists"] = feeds_df.path.apply(os.path.exists)
    return feeds_df


def download_feeds_by_author(author, feeds_df):
    for idx, row in tqdm.tqdm_notebook(list(feeds_df[feeds_df.author == author].iterrows())):
        if not os.path.exists(row.path):
            try:
                urllib.request.urlretrieve(row.href, row.path)
                time.sleep(1)
            except Exception as e:
                if os.path.exists(row.path):
                    new_path = row.path + ".tmp"
                    os.rename(row.path, new_path)
