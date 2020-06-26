# COVIDWaybackData
#### Scrapes historic COVID19 data from Worldometers using the Wayback Machine.

This is a python toolkit for scraping historical data of COVID-19 from [worldometers](worldometers.info/coronavirus) throught [Wayback Machine](https://archive.org/web/).
It uses the [Scrapy](https://scrapy.org/) framework with [scrapy-wayback-machine](https://github.com/sangaline/scrapy-wayback-machine) middleware.

This is currently a personal tool created to evaluate the relationship between number of tests and cases in Brasil. Any contribution to make it more general is welcome, there's a todo list at the end of this document.

**REQUIREMENTS**

```
pip install scrapy
pip install scrapy-wayback-machine
pip install matplotlib
pip install numpy
```

**SCRAPING**

To run the scraper use the scrapy spider as shown below. The output is saved to `scraper/output/data.tsv`.

```
cd scraper
python -m scrapy crawl worldometers
```

The time range can be set on file `scraper/settings.py`. The format is "YYYYMMDD".

```
WAYBACK_MACHINE_TIME_RANGE = ("20200505", "20201230");
```

**CLEANING**

Wayback machine data is inconsistent due to historical changes in the original table layout. I've fixed those manually using Google Sheets, but they are easy to map and should be easily fixed on parse with time range rules.

I saved the consistent data as `data/preprocess_data.py`.

To remove duplicates and then take the last timestamp of each day, run:

```
python cleaner.py
```

The filtered data is saved as `data/clean_data.py`.

**PLOTTING**

There's a python script to plot the testing data I used on my research.

```
python plot.py
```

The images are output to `plot/`.

**TODO**
- Set scraper output throught CLI
- Set scraper time range throught CLI
- Set country throught CLI (currently defaults to Brasil)
- Account for historical inconsistencies while parsing (worldometer spider)
- Set `cleaner.py` input/output throught CLI
- Set `plot.py` input/output throught CLI
