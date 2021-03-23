# Search Data Collection

Access data from search API's such as Google Custom Search and Bing
Search API from REST response to a .csv file or DataFrame.

## Installation

*Requirements:*

pandas

requests

## How To

Carry out each search using command line arguments.

An example of how to use via a command line with the Google Search API to search for "wikipedia" is below.


```
python main.py -api "google" -query "wikipedia" -key "PATH_TO_key.txt" -id "PATH_TO_id.txt"
```

Command line arguments include:

```
-api
```
type=str 

value= "bing" or "google"
Search API to be used i.e. bing or google

```
-query 
```
type=str 

Search term for the API

```
-key
``` 
type=str

Path to a text file containing your API key for the specific search API

``` 
-id 
``` 
type=str default=None 

Path to a text file containing Search Engine ID for Google Search API. Not used with Bing Search API.

``` 
-title 
``` 
type=int default=1 

Include title of search term in output

``` 
-snippet 
``` 

type=int default=1 value= 1 or 0
Include snippet of search result in output

``` 
-url 
``` 
type=int default=1 value= 1 or 0

Include url of search results in output

## Licence
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
