"""
MIT License

Copyright (c) 2021 Arbri Chili

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from data_collection.Query import Query
from data_collection.Processing import Processing
from data_collection.rest_request import read_txt
import argparse
import time
import os
import pathlib


def generate_urls(search_term, api, key_file, id_file):
    query = Query(search_term)
    try:
        key = read_txt(key_file)
        engine_id = read_txt(id_file)
        if api == "google":
            return query.google_queries(key, engine_id)
    except TypeError:
        print("No key or id file found")

    try:
        read_txt(key_file)
        if api == "bing":
            return query.bing_queries()
    except TypeError:
        print("No key file found")
        exit()


def make_request(url_list, api, title, snippet, url, key_file):
    processing = Processing(url_list, api, title, snippet, url, key_file)
    return processing.get_requests()


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-api", type=str, help="Search API to be used (i.e. bing or google)")
    parser.add_argument("-query", type=str, help="Search term for the API")
    parser.add_argument("-key", type=str, help="Text file containing API key")
    parser.add_argument("-id", type=str, default=None, help="Search Engine ID file for Google Search API")
    parser.add_argument("-title", type=int, default=1, help="Include title of search term in output")
    parser.add_argument("-snippet", type=int, default=1, help="Include snippet of search result in output")
    parser.add_argument("-url", type=int, default=1, help="Include url of search results in output")

    return parser.parse_args()


def map_to_bool(num):
    mapping = {
        1: True,
        0: False
    }
    return mapping[num]


def main():
    folder_path = pathlib.Path(__file__).parent.absolute()
    if not os.path.exists("data"):
        os.makedirs("data")
    folder_path = os.path.join(folder_path, "data")
    # Arguments
    args = arg_parser()
    search_term = args.query
    api = args.api
    key_file = args.key
    id_file = args.id
    title = map_to_bool(args.title)
    url = map_to_bool(args.url)
    snippet = map_to_bool(args.snippet)

    # Make Rest Request and save
    rest_urls = generate_urls(search_term, api, key_file, id_file)
    df = make_request(rest_urls, api, title, snippet, url, key_file)

    t = time.localtime()
    current_time = time.strftime("%d-%m-%Y_%H_%M_%S", t)
    filename = current_time + search_term + ".csv"
    filepath = os.path.join(folder_path, filename)

    if not os.path.exists(filepath):
        f = open(filepath, "x")
        f.close()
    df.to_csv(filepath)


if __name__ == '__main__':
    main()
