# Search Data Collection

Access data from search API's such as Google Custom Search and Bing
Search API.

## Installation

*Requirements:*

pandas

requests

## How to use

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