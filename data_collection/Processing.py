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

from data_collection.rest_request import get_data_from_bing, get_data_from_google
from data_collection.rest_request import read_txt
from time import sleep
import pandas as pd


class Processing:

    def __init__(self, url_list, api_type, title, snippet, url, key_file):
        self.url_list = url_list
        self.api_type = api_type
        self.title = title
        self.snippet = snippet
        self.url = url
        self.api_dictionary = {
            "google": self.get_google_request,
            "bing": self.get_bing_request
        }
        if self.api_type == "bing":
            try:
                self.key = read_txt(key_file)
            except NameError:
                print("No key file found")
                exit()

    def get_requests(self):
        data = self.api_dictionary[self.api_type]()
        col_names = self.get_col_names()
        df = pd.DataFrame(data, columns=col_names)
        return df

    def get_google_request(self):
        data_list = []
        for url in self.url_list:
            data = get_data_from_google(url)
            try:
                for d in data['items']:
                    search_result = []
                    if self.title:
                        search_result.append(d['title'])
                    if self.url:
                        search_result.append(d['link'])
                    if self.snippet:
                        search_result.append(d['snippet'])
                    data_list.append(search_result)
            except KeyError:
                print("Error in reading JSON data")
        return data_list

    def get_bing_request(self):
        data_list = []
        for url in self.url_list:
            data = get_data_from_google(url)
            try:
                for d in data['webPages']['value']:
                    search_result = []
                    if self.title:
                        search_result.append(d['name'])
                    if self.url:
                        search_result.append(d['url'])
                    if self.snippet:
                        search_result.append(d['snippet'])
                    data_list.append(search_result)
            except KeyError:
                print("Error in reading JSON data")
        return data_list

    def get_col_names(self):
        col_names = []
        if self.title:
            col_names.append("title")
        if self.url:
            col_names.append("url")
        if self.snippet:
            col_names.append("snippet")
        return col_names
