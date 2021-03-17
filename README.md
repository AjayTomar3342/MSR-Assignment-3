# MSR-Assignment-3
Mining Software Repositories follow-up project to tackle external threat to MSR-Assignment-2 Project. 

An external validity addressing project as part of the MSR course at MSR course 2020/21 at UniKo, CS department, SoftLang Team 

Please cite the following paper if you intend to know more about the original research 

>  **Is Developer Sentiment Related to Software Bugs: An Exploratory Study on GitHub Commits**
  https://ieeexplore.ieee.org/document/9054801
  
> **DBLP Link:**
  https://dblp.org/rec/conf/wcre/HuqSS20.html

## Baseline:

### Requirements:

To run this project, you will need Python3+, pip and Git installed on the system. 

The reference links are provided below.

> **Python:**
  https://www.python.org/downloads/
  
> **pip:**
  https://pypi.org/project/pip/

> **Git:**
  https://git-scm.com/downloads
	
The necessary libraries and packages are specified in the **requirements.txt** file and will be validated in the below steps


## Process for acquiring the results: 

  * **Step 1:**
  Create a local directory in your machine where you want to pull the git project and clone the project by running the below command from cmd 
  (Make sure that you are in the newly created directory first!):
  
  	```git clone https://github.com/AjayTomar3342/MSR-Assignment-3```

  * **Step 2:**
  From cmd, move into the main folder of the cloned project
  
 	 ```cd MSR-Assignment-3```

  * **Step 3:**
  Execute the below commands to meet the pre-requisites to execute the code
  
  ```  	
      Unix/macOS
      python -m pip install -r requirements.txt

      Windows
      py -m pip install -r requirements.txt
  ```

  * **Step 4:**
  On satisfying the above requirements, move into the Process folder
  
	 ```cd Process```
  
  * **Step 5:**
  Execute the below commands to run the code from cmd
  
  ``` 
      Unix/macOS
      python MSR_Assignment.py

      Windows
      %run MSR_Assignment.py
  ```
  
  
  **NOTE:** 
  After each run of the code, the **Guava Repository** Folder from the Process folder has to be deleted manually as for each run, GitHub API scrapes updated data and for successfull scraping, older data has to be deleted
  
  

## Alternative Process for acquiring the results(Backup):

For quick running of program, PyCharm use is suggested as it has good controls for removing manual steps to pull a repository and get it running.

Steps are:

  * **Step 1:**
  Make sure one is signed in on Github in Pycharm
  
  * **Step 2:**
  Open a new project
  
  * **Step 3:**
  Go to VCS Option on the Top Horizontal Options Bar
  
  * **Step 4:**
  Select Enable Version Control Integration Control inside VCS if not done already
  
  * **Step 5:**
  After checking the previous option on, select Checkout from Version Control and select Git
  
  * **Step 6:**
  In the new pop up window, include the link of the github repository you are trying to pull.
  Subsequently in the same pop up window, select an appropriate directory where the  project will be pulled.
  
  * **Step 7:**
  Select clone option to start the pulling process.
  
  * **Step 8:**
  Select option to start the pulled project in New Window or This window as per your personal preference.
  
  * **Step 9:**
  After this the project will be up and running and requirements.txt file will automatically install required libraries. Run the file MSR-Assignment.py from Process Folder to get the results

This is a quick process to start the testing of GitHub project taken from the Official Jet Brains Website. We have tried this with several PC’s and are confident that this will not give any errors.

> **Link to Above Process Video:**
  https://www.youtube.com/watch?v=ukbvdF5wqPQ&feature=emb_title


## Results:

Results are stored in an excel file inside Doc Folder named Results.xlsx. The information stored was taken from program console and was taken after the code was run on 30/1/2021 10:08:00 PM IST.

Screenshots of Results are as follows:

<img src="Data/Result_2.png"> 
<img src="Data/Result_1.png"> 


## Data Flow

The scraped data flows as per the below methodology

<img src="Data/DataFlow.png"> 


## Validation: 

Input File (acquired after scraping GitHub Repository) is named as Guava_Commit_Raw.csv and an Output File (Results.xlsx) for viewing the input and output without execution. 

Check the generated output files in the below order to validate and understand the result

**1) Guava_Commits_Raw.csv** - The cloned repository commit messages - Input File

**2) Guava_Cleaned_Commits.csv** - The cleaned commit messages

**3) Guava_Commits_Categorized.csv** - The categorised messages

**4) Guava_Commits_Cleaned_Final.csv** - The clean data after categorisation

**5) Guava_Sentiment_Scores.csv** - The sentiment values for each message

**6) Guava_Commits_Final.csv** - The final output which will be used for statistical analysis including the categories and the sentiment values

**7) Results.xlsx** – The final statistical inference - Output File


## Data: 

Input data is the extracted messages from the cloned repository, the remaining files created as part of the program are all intermediate files.

### Final statistical results

The final results are printed as part of the console

**All Emotions - Rank Sum - Pvalue:**

<img src="Data/All_Emotions_RankSum_pvalue.png">

**All Emotions Pvalue - Bonferroni Correction:**

<img src="Data/All_Emotions_Bonferroni.png">

**Polar Emotions - Rank Sum - Pvalue:**

<img src="Data/Polar_Emotions_RankSum_pvalue.png">

**Polar Emotions Pvalue - Bonferroni Correction:**

<img src="Data/Polar_Emotions_Bonferroni.png">

**Mean Values:**

<img src="Data/Mean_Values.png">

**Chi-Squared Statistics - Negative vs Positive:**

<img src="Data/Chi_Square_Negative_Positive.png">

**Chi-Squared Statistics - Emotion vs Neutral:**

<img src="Data/Chi_Square_Emotion_Neutral.png">


## Delta: 

### Process delta: 

* The original process followed in the research paper applies to 13 different huge GitHub repositories to collect a strong inference on the actual research. With respect to reproducing the research, we have applied the research steps on only 1 repository to avoid scalability issues. 

* The sentiment analysis performed in the original research paper involves Senti4SD tool but due to corrupted jar file issue within the Senti4SD code, we chose to alternatively go for NLTK Vader Sentiment analysis. In addition, NLTK Vader Sentiment Analysis sentiment scores for GitHub Commits (which were in the form of floating numbers ranging from [-1,1] were rounded up to -1/1(0 was pre-defined by the tool) as the output sentiment scores of GitHub Commits in original research process gave output in form of -1/0/1 for Negative, Neutral and Positive Sentiments for each GitHub Commit respectively.

* Mann-Whitney U Test (aka, Wilcoxon Rank Sum Test) has been implied on the data for statistical analysis despite the fact that Wilcoxon Rank Sum Test was used in the research paper since both are officially the same. Both are known to produce similar results but with minute differences.

### Data delta: 

* Due to no underlying piece of code in the research paper, we have developed the code from scratch using Python and its libraries to perform pre-processing, categorization, sentiment analysis and statistical analysis on the input data. 

* Among the multiple categories in which the data was split into, we have left out the non-FIF FC category as there was no clear understanding about this categorization in the paper and we were not ready to try out the categorization on the basis of our assumption.

* The p-values resulting from Bonferroni corrections is mostly 1 which means that the Mean values of the comparing data is almost same. This is inevitable as there is minor difference between the sentiment values among the different categories.

* The result in the research paper involves a combination of 13 huge repositories wherein we assume that the results that we got from our reproduction project is different since we considered only one medium sized repository for this task and that the repository might be biased.
