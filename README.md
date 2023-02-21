# NBA Web Scrape Project

Using guidance from DataQuest I attempted their NBA web scrape project. The aim of the project was to use Playwright to scrape 7 seasons of NBA box scores to be able to train
a machine learning model with. Libraries used were Playwright, BeautifulSoup, pandas, and for the machine learning we took advantage of sklearn.

box_score_scrape.py - is the code for the web scrape portion, I wasn't able to run in Jupyter Notebooks because async playwright is buggy on Windows for some reason, so just
wrote the code in a normal python script using sync playwright

parse_box_scores.ipynb - notebook containing code to clean data and structuring it in a pandas DataFrame so it's easy for models to work with 

predictions.ipynb - code for machine learning models. Able to get up 63% accuracy but tinkering with different features and models could improve accuracy score
