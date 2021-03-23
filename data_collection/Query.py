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


class Query:
    def __init__(self, query):
        self.query = query

    def get_query(self):
        return self.query

    def google_queries(self, key, search_id):
        url_array = []
        # Maximum number of 100 search terms can be found by Google Custom Search API. Only 10 terms can be found per
        # URL request. Therefore 10 URLs have to be generated with staggered search term start indexes to obtain up
        # to a maximum of 100 results.
        for i in range(1, 2, 10):
            url = "https://www.googleapis.com/customsearch/v1?key=" + key + "&cx=" + search_id + "&start=" + str(i) + \
                  "&q=" + self.query
            url_array.append(url)
        return url_array

    def bing_queries(self):
        # Trial and error found these values to get best results
        count = 40
        num_of_urls = 20

        index = 0
        url_array = []   # label what search engine the array comes from.
        for i in range(1, num_of_urls + 1):
            url = "https://api.cognitive.microsoft.com/bingcustomsearch/v7.0/search?&q=" + self.query + \
                  "&customConfig=2&offset=" + str(index) + "&count=" + str(count)
            url_array.append(url)
            index += count
        return url_array
