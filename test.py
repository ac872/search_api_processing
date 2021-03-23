import json
import requests
import urllib.request
from time import sleep
import string
import nltk  # Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly
# Media Inc.
import csv
import glob
import os
import pandas as pd
import ast
from src.FileHandling.Files import Files
from src.Modules.df_modules import read_csv_to_data_frame
from urllib.parse import urlparse
from langdetect import detect, DetectorFactory


class FileConverter(Files):
    """
    FileConverter Class. Inherits from SuperClass Files.
    Used to process JSON files created by the JSONFileCreator Class into CSV files as well as other processing steps
    such as text processing and language processing.
    """

    def __init__(self):
        """
        Inherit filenames and locations and some naming functions from the Files Class. These are so that the two
        classes FileConverter and JSONFileCreator can read the same files to be able to convert from .json format to
        .csv successfully.

        """

        super().__init__()

    def convert_json(self, query):
        """
        Called to convert .json files to .csv files. The same query name is obtained for the generation of the JSON
        data as well as for the conversion of the data. Can be used for both the Bing and Google Search API's and
        determines what type of conversion is required based off the file names, so it calls the specific function
        that is appropriate for the specific API. The .json files are immediately deleted after use allowing for the
        next conversion after the next search to not repeat the same results obtained.
        :param query: str
        """

        if os.path.exists(self._json_directory + "0" + self._google_file_name):
            self.convert_google_json(query)
        if os.path.exists(self._json_directory + "0" + self._bing_file_name):
            self.convert_bing_json(query)
        else:
            print("No relevant files found, please create files and try again.")

    def convert_google_json(self, query):
        """
        Reads .json files returned by the Google Custom Search API and extracts the title, snippet and URL from each
        of the search results obtained in the specific way that is required by the Google Search API. A unique index
        is also added to each of the search results and then this information is written to a csv file with name of
        the search term or "query" used to generate the search data. The .json files are then deleted.
        :param query: str
        """

        # Create a new CSV containing the results for the search. The actual search term will be used as the file name.
        with open(self.csv_name(query), "w+", encoding="utf8") as csv_file:
            file = csv.writer(csv_file)
            file.writerow(["index", "title", "url", "url-netloc", "snippet"])
            i = 1
            for filename in sorted(glob.iglob(self._json_directory + "**/*google.json", recursive=True)):
                with open(filename, encoding="utf8") as json_file:
                    data = json.load(json_file)
                try:
                    for d in data["items"]:
                        title = d["title"]
                        link = d["link"]
                        snippet = d["snippet"]
                        file.writerow([i, self.process(title), link, urlparse(link).netloc,
                                       self.process(snippet)])
                        i += 1
                except KeyError:
                    print("JSON file does not contain 10 results")
            for file_to_delete in sorted(glob.iglob(self._json_directory + "**/*.json", recursive=True)):
                os.remove(file_to_delete)

    def convert_bing_json(self, query):
        """
        Reads .json files returned by the Bing Search API and extracts the title, snippet and URL from each
        of the search results obtained in the specific way that is required by the Bing Search API. A unique index
        is also added to each of the search results and then this information is written to a csv file with name of
        the search term or "query" used to generate the search data. The .json files are then deleted.
        :param query: str
        """

        with open(self.csv_name(query), "w+") as csv_file:
            file = csv.writer(csv_file)
            file.writerow(["index", "title", "link", "snippet"])
            i = 1
            for filename in sorted(glob.iglob(self._json_directory + '**/*bing.json', recursive=True)):
                with open(filename) as json_file:
                    data = json.load(json_file)
                    for d in data['webPages']['value']:
                        title = d['name']
                        link = d['url']
                        snippet = d['snippet']
                        file.writerow([i, self.process(title), link, self.process(snippet)])
                        i += 1
                os.remove(filename)

    def combine_csv_with_index(self):
        """
        Combines all csv files in the specified csv directory in the Files Class into one csv file and writes it to
        a specified location. Used mainly for collecting and combining the large number of search terms during the data
        phase collection of the project. However, it can now be used to combine all the new searches so that you have
        all searches saved.
        """

        filenames = glob.iglob(self._csv_directory + "**/*.csv", recursive=True)
        data_frame = pd.concat((pd.read_csv(file, engine="python") for file in filenames))
        keep_col = ["index", "title", "url", "snippet"]
        new_f = data_frame[keep_col]
        new_f.reset_index(drop=True, inplace=True)
        new_f.to_csv(self._combined_csv, index=True)

    @staticmethod
    def get_random_sample(random_sample_size, file_name):
        """
        Return a random sample of CSV data rows in a combined CSV file. Will return an indexed data frame.
        ValueError if you select a larger sample size than the number of rows in the CSV file.

        :param file_name: str
        :param random_sample_size: int
        :return: list
        """

        data_frame = pd.read_csv(file_name, header=0, index_col=0)
        try:
            data_frame = data_frame.sample(random_sample_size)
            data_frame.reset_index(inplace=True, drop=True)  # Reset Indexes to start from 0
            return data_frame
        except ValueError:
            print("ValueError: Cannot take a larger sample than population when 'replace=False'\nPlease Try Again")
        except TypeError:
            print("TypeError: Incorrect Data Type, Please use an integer")

    @staticmethod
    def process_language(file_name):
        """
        Read a file of file_name, combine the titles and snippets of the search results in the file. Test the combined
        title and snippet for each search result attach a label to each result as either English or non-English.
        Discard all non-English search results and return the search results that are in English as a DataFrame.
        :param file_name: str
        :return: DataFrame
        """

        df = read_csv_to_data_frame(file_name)
        language = []
        for index, row in df.iterrows():
            title = row['title']
            new_title = [new_title.strip() for new_title in ast.literal_eval(title)]
            title_text = ""
            snippet = row['snippet']
            new_snippet = [new_snippet.strip() for new_snippet in ast.literal_eval(snippet)]
            snippet_text = ""
            for word in new_title:
                title_text += " " + word
            for word in new_snippet:
                snippet_text += " " + word
            text = title_text + " " + snippet_text
            DetectorFactory.seed = 0  # Force consistent algorithmic language determination
            if detect(text) == "en":
                language.append("en")
            else:
                language.append("non-en")
        df['language'] = language
        df = df[df.language == "en"]
        return df

    @staticmethod
    def read_csv_file(filename):
        """
        Read a .csv file and return a list of lists of the rows in the .csv file.
        :param filename: str
        :return: list
        """

        with open(filename, 'r', encoding="utf8") as outfile:
            reader = csv.reader(outfile)
            csv_rows = [row for row in reader]
        return csv_rows

    def process(self, sentences):
        """
        Combine all of the text processing required into one callable function and return the processed text.
        :param sentences: str
        :return: str
        """
        return self.tokenize(self.remove_punctuation(sentences))

    @staticmethod
    def remove_punctuation(sentences):
        """
        Remove punctuation from sentences.
        :param sentences: str
        :return: str
        """

        return sentences.translate(str.maketrans("", "", string.punctuation)).lower()

    @staticmethod
    def tokenize(sentences):
        """
        Tokenize words.
        :param sentences: str
        :return: str
        """

        return nltk.word_tokenize(sentences)


def process_text(text):
    """
    Process text to remove punctuation and stopwords and return the processed text. Extra processing that is required
    for the LSTM model.
    :param text: str
    :return: str
    """
    text_to_replace = re.compile('[/(){}\[\]\|@,;^0-9#+_]')
    stop_words = set(stopwords.words("english"))
    text.lower()
    text = text_to_replace.sub(" ", text)
    text = " ".join(word for word in text.split() if word not in stop_words)
    return text