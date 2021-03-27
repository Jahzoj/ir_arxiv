#!usr/env/bin

import os
import sys
import getopt
import getopt

import arxivscraper as ax
import pandas as pd

def write_chunks(data,filename,chunksize):
    if not os.path.exists(filename):
        with open(filename, "w"):
            print("creating file...")

    start = 0
    end = min(chunksize,data.shape[0])
    data.loc[0:0,:].to_csv(filename, index=False, encoding='utf-8')

    while(True):
        if(start == end):
            break    

        chunk = data.loc[start:end - 1,:]
        chunk.to_csv(filename, index=False, header=False, mode="a", encoding='utf-8')

        end = min(end+chunksize,data.shape[0])
        start = min(start+chunksize,data.shape[0])

    return 0

def download():
    argv = ["filename","category","date_from","date_until"]
    opts = ["help","options"]
    categories = ["cs","econ","eess","math","physics",
    "physics:astro-ph","physics:cond-mat","physics:gr-qc",
    "physics:hep-ex","physics:hep-lat","physics:hep-ph",
    "physics:hep-th","physics:math-ph","physics:nlin","physics:nucl-ex",
    "physics:nucl-th","physics:physics","physics:quant-ph","q-bio",
    "q-fin","stat"]

    try:
        opts, argv = getopt.getopt(sys.argv[1:],"ho",["help","options"])
    except getopt.GetoptError:
        print("opt error")
        sys.exit(2)

    for opt in opts:
        if opt[0] in ('-h', '--help'):
            print("Usage: arxiv_download.py <filename> <category> <date_from = YYYY-MM-DD> <date_until = YYYY-MM-DD>")
            sys.exit()
        if opt[0] in ('-o', '--options'):
            print("list of categories: {}".format(categories))
            sys.exit()

    if (len(argv) != 4):
        print("not enough arguments")
        sys.exit(2)

    scrp = ax.Scraper(category = sys.argv[1], date_from = sys.argv[2], date_until = sys.argv[3])  
    data = scrp.scrape()

    cols = ('id', 'title', 'categories', 'abstract', 'doi', 'created', 'updated', 'authors')
    df = pd.DataFrame(data,columns=cols)
    
    file_name = os.path.join(os.getcwd(),"{}.csv".format(sys.argv[1]))
    write_chunks(df,file_name,2)

    print("finished downloading {} papers".format(df.shape[0]))

if __name__ == "__main__":
    download()
