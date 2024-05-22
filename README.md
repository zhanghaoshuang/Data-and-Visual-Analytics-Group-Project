# CSE6242 Final Project 

### Description 
Our project analyzes the dataset that Yelp provides (https://www.yelp.com/dataset) with businesses, reviews, tips, and checkins to determine supply and demand of individual businesses and infer future business opportunities. 

### Running Our Code 

#### Loading the Data into SQL and Filtering to Only Philadelphia Businesses 

1. Download the Yelp dataset from the website above. It comes as two archive files: `yelp_dataset.tar` and `yelp_photos.tar`. Extract the archive files into `./data` folder to obtain the following JSON files listed below:
    * `./data/yelp_academic_dataset_business.json`,
    * `./data/yelp_academic_dataset_checkin.json`,
    * `./data/yelp_academic_dataset_review.json`,
    * `./data/yelp_academic_dataset_tip.json`,
    * `./data/yelp_academic_dataset_user.json`,
    * `./data/photos.json`;

2. Download & install PostgreSQL, create a username and password, then create a database called `yelp` and a schema under the database called `yelp_ds`

3. Run the following SQL file create_yelp_ds in the data folder to create the database schema: `create_yelp_ds.sql`

4. Install most recent version of Python 3. Once it is done please setup your Python virtual environment using one of your favorite virtual environment tools (conda, virtualenv, poetry etc.) and install PostreSQL driver for Python:
```
$ pip3 install psycopg2-binary
```

5. Run the following python scripts to load the JSON data files into the PostgreSQL database. Note please make sure that we have JSON data files stored in the same folder with these scripts.
    1. `python3 ./1_load_businesses.py`,
    2. `python3 ./1_load_users.py`,
    3. `python3 ./2_load_checkins.py`,
    3. `python3 ./2_load_photos.py`,
    4. `python3 ./2_load_reviews.py`,
    5. `python3 ./2_load_tips.py`;

Note: please make sure that the python scripts listed above have proper connectivity settings configured for SQL database like it is shown on the code snippet below. You might want to change username and host and add a password if you run PostreSQL on a different host:
```
with psycopg2.connect(database = "yelp", user = "vorlov", host= "localhost", port = 5432, options="-c search_path=yelp_ds") as conn:
```


6. Once the files have been loaded in the database, you can proceed to the next sections to analyze the data.

7. For the PostgreSQL dattabase created above, please run the following script: `./data/4_prefiltered_data.sql`. This will filter the data to only include Philadelphia data and create additional tables for it: 
    * PHI_BUSINESS,
    * PHI_CUSTOMER,
    * PHI_REVIEW,
    * PHI_TIP,
    * PHI_CHECKIN.

#### Clustering to Find Business Categories 
1. From the preproccessing folder, run `preprocess-categories.ipynb` to produce `philly_categories_v2.csv` which is the phi_business dataframe but with business categories for each business. Note: we extracted business categories into a SQL script `data/6_categories.sql`, which is used later to upload them into the database.

#### Calculating Demand and Missing Demand Score
1. Please use the following SQL query to compute the total demand & missing demand scores by business:
```
data/5_compute_demand_scores.sql
```

2. In order to roll up total demand & missing demand scores, please load business categories into database first using the following SQL script:
```
data/6_categories.sql
```

3. Once business categories are loaded into the database, please use the following SQL query to compute total demand & missing demand score roll ups by zip code and business category:
```
data/7_compute_demand_scores_by_zip_bicategory.sql
```
The results of this SQL query can then be exported into CSV format for subsequent visualization in Tableau.

#### NLP
*NOTE:* all required libraries are in the `requirements.txt` file. Versions should just be updated to the latest versions of each package: 

- matplotlib
- seaborn
- numpy
- pandas
- nltk
- sklearn
- wordcloud

*NOTE:* Notebooks are used for experimentation, score creation and processing text. Thus run times may be upwards to >45+ minutes on certain cells. CSVs created are also >1 GB, thus no CSVs are included in the repo due to size limitations.

1. `8_combine_reviews_business_categories.sql` in the data folder contains the SQL required to combine review information along with category and zipcode. It's recommended to download CSVs in 3-4 parts for further analysis due to size

2. `NLP-v1.ipynb` contains initial preprocessing for word tokenization and initial wordclouds/EDA 

3. Further experimenation and processing to get word frequencies as well as the VADER sentiment scores was performed in `NLP-v2.ipynb`

4. N-gram analysis was completed and processed further for tableau compatibility in `NLP-v3.ipynb` and `NLP-v4.ipynb`

#### Experiment, Evaluating Our Demand and Missing Demand Score
1. From the experiment folder, run the SQL file `download_phi_review.sql` and `Download_NO_review.sql` (need to change the directory to whatever folder you are saving the jupyter notebook files to). This will create two csv files, `phi_review.csv` and `no_review.csv`

2. Download all the files in the experiment folder (csv and jupyter notebook) into the same directory that you chose for above (1)

3. Run the jupyter notebook files (`Philly_Experiment.ipynb` and `NewOrleansExperiment.ipynb`) and they will display the results of the evaluation of our demand and missing demands scores 


#### Tableau Visualization

1. We built a dashboard to visualize the businesses' demand and other insights from the Yelp Data. Use the following link to access the dashboard: https://public.tableau.com/app/profile/shivani.narahari/viz/YelpDemandDashboard/Dashboard1?publish=yes
