from git import Repo
import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from scipy.stats import ranksums
from scipy.stats import chi2_contingency
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
import statsmodels.stats.multitest as multi

##Guava
#Clone guava repository
guava_repo=Repo.clone_from("https://github.com/google/guava.git", "Guava Repository")

#Get all the commits details from Guava Repository
guava_commits = list(guava_repo.iter_commits('master'))

#Get all commit messages with revision-id's from Guava Repository
guava_commits_messages=list([{'code':str(c),'message':str(c.message)} for c in guava_commits])

#Create pandas dataframe for Guava Repository Commit messages
guava_commits_raw_df=pd.DataFrame({'Commit Messages':guava_commits_messages})

###Zsh
#Clone zsh repository
zsh_repo=Repo.clone_from("https://github.com/zsh-users/zsh", "Zsh")

#Get all the commits details from zsh Repository
zsh_commits = list(zsh_repo.iter_commits('master'))

#Get all commit messages with revision-id's from zsh Repository
zsh_commits_messages=list([{'code':str(c),'message':str(c.message)} for c in zsh_commits])

#Create pandas dataframe for Zsh Repository Commit messages
zsh_commits_raw_df=pd.DataFrame({'Commit Messages':zsh_commits_messages})

###Power Shell

#Clone power shell repository
power_shell_repo=Repo.clone_from("https://github.com/PowerShell/PowerShell", "Power Shell")

#Get all the commits details from power shell Repository
power_shell_commits = list(power_shell_repo.iter_commits('master'))

#Get all commit messages with revision-id's from power shell Repository
power_shell_commits_messages=list([{'code':str(c),'message':str(c.message)} for c in power_shell_commits])

#Create pandas dataframe for Power Shell Repository Commit messages
power_shell_commits_raw_df=pd.DataFrame({'Commit Messages':power_shell_commits_messages})

print("Guava",len(guava_commits_raw_df))
#Append all data frames
guava_commits_raw_df=guava_commits_raw_df.append(zsh_commits_raw_df)
guava_commits_raw_df=guava_commits_raw_df.append(power_shell_commits_raw_df)

print("Zsh",len(zsh_commits_raw_df))
print("Power Shell ",len(power_shell_commits_raw_df))

#Save pandas dataframe as csv file
guava_commits_raw_df.to_csv('../Data/Guava_Commits_Raw.csv')

# Read in commit message file
guava_df = pd.read_csv('../Data/Guava_Commits_Raw.csv', index_col=0)

pd.set_option("display.max_colwidth", 1)

guava_df=guava_df.reset_index()

# Split commit messages and revision id
guava_split_df = guava_df['Commit Messages'].str.split(",", 1, expand=True)

# Assign column names
guava_split_df.columns = ['Commit', 'Messages']

guava_split_df[['Commit']] = guava_split_df.Commit.str.split('\"', expand=True)
# guava_split_df = guava_split_df.drop(['1', '4'], axis=1)

# Save pandas dataframe as csv file
guava_split_df.to_csv('Guava_Commits_Cleaned.csv')

# Search based on keywords to categorize FC commits
for msg in guava_split_df['Messages']:
    if 'Fix ' in msg or ' fix' in msg or 'Bug ' in msg or ' bug' in msg or 'Patch ' in msg or ' patch' in msg:

        ######Uncomment the following commented lines and add in the if check statement to check the impact of adding new terms

        #or 'Fail' in msg or 'fail' in msg or 'tweak' in msg or 'Tweak' in msg or ' cat' in msg or 'Cat' in msg or
        # 'Typo' in msg or 'Missing' in msg or 'missing' in msg or 'typo' in msg or ' patch' in msg or 'Correct' in msg
        # or 'correct' in msg or 'Error' in msg or 'error' in msg or 'Avoid' in msg or 'avoid' in msg or 'Fail' in msg
        # or 'fail' in msg:
        guava_split_df.loc[guava_split_df.Messages == msg, "Category"] = 'FC'
    else:
        guava_split_df.loc[guava_split_df.Messages == msg, "Category"] = ''

# Assigning FC to new dataframe to do further filterations
guava_df_with_fc = guava_split_df[guava_split_df['Category'] == 'FC']

# Identifying documentation from FC
for msg in guava_df_with_fc['Messages']:
    if 'comment' in msg or 'assertion' in msg or 'doc' in msg:
        guava_df_with_fc.loc[guava_df_with_fc.Messages == msg, "Category"] = 'Documentation-FC'

# Remove insert from FC's
guava_df_with_fc_and_without_documentation = guava_df_with_fc[guava_df_with_fc['Category'] == 'FC']

for msg in guava_df_with_fc_and_without_documentation['Messages']:
    if 'insert' in msg:
        guava_df_with_fc_and_without_documentation.loc[
            guava_df_with_fc_and_without_documentation.Messages == msg, "Category"] = 'Insert-FC'

# Get pure FC's
guava_df_with_final_fc = guava_df_with_fc_and_without_documentation[
    guava_df_with_fc_and_without_documentation['Category'] == 'FC']

# Joining FC commits with the original dataframe
guava_df_fc = pd.concat([guava_split_df, guava_df_with_final_fc["Category"]], axis=1)

# Removing old category column
# Rename the same column name before removal
guava_df_fc.columns = ['Commit', 'Messages', 'Old', 'Category']
del guava_df_fc['Old']

guava_df_fc.fillna('', inplace=True)

# Categorize messages for FIC and FIF
for i in guava_df_fc['Category'].index.values:
    if guava_df_fc['Category'][i] == 'FC':
        fic_index = guava_df_fc['Category'].index[i + 1]
        if guava_df_fc.loc[guava_df_fc['Category'].index[fic_index], 'Category'] == '':
            guava_df_fc.loc[guava_df_fc['Category'].index[fic_index], 'Category'] = 'FIC'
        elif guava_df_fc.loc[guava_df_fc['Category'].index[fic_index], 'Category'] == 'FC':
            guava_df_fc.loc[guava_df_fc['Category'].index[fic_index], 'Category'] = 'FIF'

# Categorize messages for pFIC
for i in guava_df_fc['Category'].index.values:
    if guava_df_fc['Category'][i] == 'FIC' or guava_df_fc['Category'][i] == 'FIF':
        pfic_index = guava_df_fc['Category'].index[i + 1]
        if guava_df_fc.loc[guava_df_fc['Category'].index[pfic_index], 'Category'] == '':
            guava_df_fc.loc[guava_df_fc['Category'].index[pfic_index], 'Category'] = 'pFIC'

        # Categorize for regular commit messages
for i in guava_df_fc['Category'].index.values:
    if guava_df_fc['Category'][i] == '':
        guava_df_fc['Category'][i] = 'Regular'

# Loading into new dataframe and save as csv file
guava_df_categorized = guava_df_fc

#Comparison Stastistics
guava_df_for_analyzing=guava_df_categorized.iloc[0:5432,]
zsh_df_for_analyzing=guava_df_categorized.iloc[5433:16865,]
power_shell_df_for_analyzing=guava_df_categorized.iloc[16866:25530,]

#Guava Statistics
print("Guava Statistics")
print(guava_df_for_analyzing.groupby('Category').count())

#Zsh Statistics
print("Zsh Statistics")
print(zsh_df_for_analyzing.groupby('Category').count())

#Power Shell Statistics
print("Power Shell Statistics")
print(power_shell_df_for_analyzing.groupby('Category').count())

#Overall Statistics
print("Overall Statistics")
print(guava_df_categorized.groupby('Category').count())

guava_df_categorized.to_csv('../Data/Guava_Commits_Categorized.csv')

#Read in commit message file
guava_df = pd.read_csv('../Data/Guava_Commits_Categorized.csv',index_col=0)

#Split commit messages column
guava_df = guava_df["Messages"].str.split("RELNOTES",expand=True)

#Delete unwanted column
del guava_df[1]

#Remove unwanted characters
unwanted_chars = ["{","\'","message :","\n'","\n\n","}",".","\nPiperOrigin-RevId:","\"","]",",","\\n\n","{'code': '"]

for char in unwanted_chars:
    guava_df[0] = guava_df[0].str.replace(char, ' ')

link='http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
     '(?:%[0-9a-fA-F][0-9a-fA-F]))+'

guava_df[0]=guava_df[0].str.replace(link,'  ')

print(guava_df)
guava_df.reset_index()
#Save pandas dataframe as csv file
guava_df.to_csv('../Data/Guava_Commits_Cleaned_Final.csv')


guava_df = pd.read_csv('../Data/Guava_Commits_Cleaned_Final.csv',index_col=0)

sentiment_scores=list()
analyzer = SentimentIntensityAnalyzer()
for i in range(0,len(guava_df['0'])):
    sentiment_scores.append(analyzer.polarity_scores(guava_df['0'][i])["compound"])

sentiment_scores_smoothed=list()

for item in sentiment_scores:
    if item < 0:
        item = -1
    elif item>0:
        item=1
    sentiment_scores_smoothed.append(item)

guava_df_sentiments = pd.DataFrame(sentiment_scores_smoothed,columns=['Sentiment Score'])

#Positive=1585
#Neutral=2866
#Negative=972

guava_df.to_csv('../Data/Guava_Cleaned_Commits.csv')
guava_df_sentiments.to_csv('../Data/Guava_Sentiment_Scores.csv')

guava_df_categorized = pd.read_csv('../Data/Guava_Commits_Categorized.csv',index_col=0)
guava_df_sentiment_scores = pd.read_csv('../Data/Guava_Sentiment_Scores.csv',index_col=0)

guava_df_complete= pd.concat([guava_df_categorized, guava_df_sentiment_scores], join = 'outer', axis = 1)

print(guava_df_complete)
guava_df_complete.to_csv('../Data/Guava_Commits_Final.csv')

guava_df = pd.read_csv('../Data/Guava_Commits_Final.csv',index_col=0)

##All Emotions Test
all_emotions_test=list()
#Get FIC's with all emotions
fic_with_all_emotions= guava_df[guava_df['Category']=='FIC']
fic_with_all_emotions=fic_with_all_emotions['Sentiment Score']

#Get non-FIC's with all emotions
non_fic_regulars_with_all_emotions= guava_df[guava_df['Category']!='FIC']
non_fic_regulars_with_all_emotions=non_fic_regulars_with_all_emotions['Sentiment Score']

print("P-Value between All emotions FIC and Regular Commits",mannwhitneyu(fic_with_all_emotions, non_fic_regulars_with_all_emotions))
all_emotions_test.append(mannwhitneyu(fic_with_all_emotions, non_fic_regulars_with_all_emotions)[1])

#Get pFIC's with all emotions
pfic_with_all_emotions= guava_df[guava_df['Category']=='pFIC']
pfic_with_all_emotions=pfic_with_all_emotions['Sentiment Score']

#Get non-pFIC's with all emotions
non_pfic_regulars_with_all_emotions= guava_df[guava_df['Category']!='pFIC']
non_pfic_regulars_with_all_emotions=non_pfic_regulars_with_all_emotions['Sentiment Score']

print("P-Value between All emotions pFIC's and Regular Commits",mannwhitneyu(pfic_with_all_emotions, non_pfic_regulars_with_all_emotions))
all_emotions_test.append(mannwhitneyu(pfic_with_all_emotions, non_pfic_regulars_with_all_emotions)[1])

#Get FC's with all emotions
fc_with_all_emotions= guava_df[guava_df['Category']=='FC']
fc_with_all_emotions=fc_with_all_emotions['Sentiment Score']

#Get non-FC's with all emotions
non_fc_regulars_with_all_emotions= guava_df[guava_df['Category']!='FC']
non_fc_regulars_with_all_emotions=non_fc_regulars_with_all_emotions['Sentiment Score']

print("P-Value between All emotions FC's and Regular Commits",mannwhitneyu(fc_with_all_emotions, non_fc_regulars_with_all_emotions))
all_emotions_test.append(mannwhitneyu(fc_with_all_emotions, non_fc_regulars_with_all_emotions)[1])

#Get FIF's with all emotions
fif_with_all_emotions= guava_df[guava_df['Category']=='FIF']
fif_with_all_emotions=fif_with_all_emotions['Sentiment Score']

#Get non-FIF's with all emotions
non_fif_regulars_with_all_emotions= guava_df[guava_df['Category']!='FIF']
non_fif_regulars_with_all_emotions=non_fif_regulars_with_all_emotions['Sentiment Score']

print("P-Value between All emotions FIF's and Regular Commits",mannwhitneyu(fif_with_all_emotions, non_fif_regulars_with_all_emotions))
all_emotions_test.append(mannwhitneyu(fif_with_all_emotions, non_fif_regulars_with_all_emotions)[1])

p_adjusted = multi.multipletests(all_emotions_test, method='bonferroni',alpha=0.05)
print("P Adjusted values for All polarity test", p_adjusted)


print(" ")
print("Polar Emotions Test")
##Only Polar Emotions Test

polar_emotions_test=[]
#Get FIC's with polar emotions
fic_with_polar_emotions= guava_df.loc[(guava_df['Category']=='FIC') & ((guava_df['Sentiment Score']==-1) | (guava_df['Sentiment Score']==1))]
fic_with_polar_emotions=fic_with_polar_emotions['Sentiment Score']

#Get non-FIC's with polar emotions
non_fic_regulars_with_polar_emotions= guava_df.loc[(guava_df['Category']!='FIC') & ((guava_df['Sentiment Score']==-1) | (guava_df['Sentiment Score']==1))]
non_fic_regulars_with_polar_emotions=non_fic_regulars_with_polar_emotions['Sentiment Score']

print("P-Value between polar emotions FIC and Regular Commits",mannwhitneyu(fic_with_polar_emotions, non_fic_regulars_with_polar_emotions))
polar_emotions_test.append(mannwhitneyu(fic_with_polar_emotions, non_fic_regulars_with_polar_emotions)[1])

#Get pFIC's with polar emotions
pfic_with_polar_emotions= guava_df.loc[(guava_df['Category']=='pFIC') & ((guava_df['Sentiment Score']==-1) | (guava_df['Sentiment Score']==1))]
pfic_with_polar_emotions=pfic_with_polar_emotions['Sentiment Score']

#Get non-pFIC's with polar emotions
non_pfic_regulars_with_polar_emotions= guava_df.loc[(guava_df['Category']!='pFIC') & ((guava_df['Sentiment Score']==-1) | (guava_df['Sentiment Score']==1))]
non_pfic_regulars_with_polar_emotions=non_pfic_regulars_with_polar_emotions['Sentiment Score']

print("P-Value between polar emotions pFIC and Regular Commits",mannwhitneyu(pfic_with_polar_emotions, non_pfic_regulars_with_polar_emotions))
polar_emotions_test.append(mannwhitneyu(pfic_with_polar_emotions, non_pfic_regulars_with_polar_emotions)[1])

#Get FC's with polar emotions
fc_with_polar_emotions= guava_df.loc[(guava_df['Category']=='FC') & ((guava_df['Sentiment Score']==-1) | (guava_df['Sentiment Score']==1))]
fc_with_polar_emotions=fc_with_polar_emotions['Sentiment Score']

#Get non-FC's with polar emotions
non_fc_regulars_with_polar_emotions= guava_df.loc[(guava_df['Category']!='FC') & ((guava_df['Sentiment Score']==-1) | (guava_df['Sentiment Score']==1))]
non_fc_regulars_with_polar_emotions=non_fc_regulars_with_polar_emotions['Sentiment Score']

print("P-Value between polar emotions FC and Regular Commits",mannwhitneyu(fc_with_polar_emotions, non_fc_regulars_with_polar_emotions))
polar_emotions_test.append(mannwhitneyu(fc_with_polar_emotions, non_fc_regulars_with_polar_emotions)[1])

#Get FIF's with polar emotions
fif_with_polar_emotions= guava_df.loc[(guava_df['Category']=='FIF') & ((guava_df['Sentiment Score']==-1) | (guava_df['Sentiment Score']==1))]
fif_with_polar_emotions=fif_with_polar_emotions['Sentiment Score']

#Get non-FIF's with polar emotions
non_fif_regulars_with_polar_emotions= guava_df.loc[(guava_df['Category']!='FIF') & ((guava_df['Sentiment Score']==-1) | (guava_df['Sentiment Score']==1))]
non_fif_regulars_with_polar_emotions=non_fif_regulars_with_polar_emotions['Sentiment Score']

print("P-Value between polar emotions FIF and Regular Commits",mannwhitneyu(fif_with_polar_emotions, non_fif_regulars_with_polar_emotions))
polar_emotions_test.append(mannwhitneyu(fif_with_polar_emotions, non_fif_regulars_with_polar_emotions)[1])
p_adjusted_polarity = multi.multipletests(polar_emotions_test, method='bonferroni',alpha=0.05)
print("P Adjusted values for All polarity test", p_adjusted_polarity)


print("FIC Mean All emotions",np.mean(fic_with_all_emotions))
print("Non-FIC Regular Mean All emotions",np.mean(non_fic_regulars_with_all_emotions))
print("pFIC Mean All emotions",np.mean(pfic_with_all_emotions))
print("Non-pFIC Regular Mean All emotions",np.mean(non_pfic_regulars_with_all_emotions))
print("FC Mean All emotions",np.mean(fc_with_all_emotions))
print("Non-FC Regular Mean All emotions",np.mean(non_fc_regulars_with_all_emotions))
print("FIF Mean All emotions",np.mean(fif_with_all_emotions))
print("Non-FIF Regular Mean All emotions",np.mean(non_fif_regulars_with_all_emotions))


print("FIC Mean Polar emotions",np.mean(fic_with_polar_emotions))
print("Non-FIC Regular Mean Polar emotions",np.mean(non_fic_regulars_with_polar_emotions))
print("pFIC Mean Polar emotions",np.mean(pfic_with_polar_emotions))
print("Non-pFIC Regular Mean Polar emotions",np.mean(non_pfic_regulars_with_polar_emotions))
print("FC Mean Polar emotions",np.mean(fc_with_polar_emotions))
print("Non-FC Regular Mean Polar emotions",np.mean(non_fc_regulars_with_polar_emotions))
print("FIF Mean Polar emotions",np.mean(fif_with_polar_emotions))
print("Non-FIF Regular Mean Polar emotions",np.mean(non_fif_regulars_with_polar_emotions))




#Chi-Squared Test-Negative Vs. Positive

#FIC vs Regular
fic_vs_regular_negative_and_positive= guava_df[(((guava_df['Category']=='FIC') | (guava_df['Category']!='FIC'))) & (((guava_df['Sentiment Score']==-1) | (guava_df['Sentiment Score']==1)))]
fic_vs_regular_negative_and_positive=fic_vs_regular_negative_and_positive[['Category','Sentiment Score']]

fic_vs_regular_negative_and_positive.loc[fic_vs_regular_negative_and_positive['Sentiment Score']== -1, 'Sentiment Score'] = "Negative"
fic_vs_regular_negative_and_positive.loc[fic_vs_regular_negative_and_positive['Sentiment Score']== 1, 'Sentiment Score'] = "Positive"
contigency= pd.crosstab(fic_vs_regular_negative_and_positive['Category'], fic_vs_regular_negative_and_positive['Sentiment Score'])

contigency_pct = pd.crosstab(fic_vs_regular_negative_and_positive['Category'], fic_vs_regular_negative_and_positive['Sentiment Score'], normalize='index')

print(" ")
print("FIC Vs. Regular")
print(contigency_pct)

#pFIC vs Regular
pfic_vs_regular_negative_and_positive= guava_df[(((guava_df['Category']=='pFIC') | (guava_df['Category']!='pFIC'))) & (((guava_df['Sentiment Score']==-1) | (guava_df['Sentiment Score']==1)))]
pfic_vs_regular_negative_and_positive=pfic_vs_regular_negative_and_positive[['Category','Sentiment Score']]

pfic_vs_regular_negative_and_positive.loc[pfic_vs_regular_negative_and_positive['Sentiment Score']== -1, 'Sentiment Score'] = "Negative"
pfic_vs_regular_negative_and_positive.loc[pfic_vs_regular_negative_and_positive['Sentiment Score']== 1, 'Sentiment Score'] = "Positive"
contigency= pd.crosstab(pfic_vs_regular_negative_and_positive['Category'], pfic_vs_regular_negative_and_positive['Sentiment Score'])

contigency_pct = pd.crosstab(pfic_vs_regular_negative_and_positive['Category'], pfic_vs_regular_negative_and_positive['Sentiment Score'], normalize='index')

print(" ")
print("pFIC Vs. Regular")
print(contigency_pct)


#FC vs Regular
fc_vs_regular_negative_and_positive= guava_df[(((guava_df['Category']=='FC') | (guava_df['Category']!='FC'))) & (((guava_df['Sentiment Score']==-1) | (guava_df['Sentiment Score']==1)))]
fc_vs_regular_negative_and_positive=fc_vs_regular_negative_and_positive[['Category','Sentiment Score']]

fc_vs_regular_negative_and_positive.loc[fc_vs_regular_negative_and_positive['Sentiment Score']== -1, 'Sentiment Score'] = "Negative"
fc_vs_regular_negative_and_positive.loc[fc_vs_regular_negative_and_positive['Sentiment Score']== 1, 'Sentiment Score'] = "Positive"
contigency= pd.crosstab(fc_vs_regular_negative_and_positive['Category'], fc_vs_regular_negative_and_positive['Sentiment Score'])

contigency_pct = pd.crosstab(fc_vs_regular_negative_and_positive['Category'], fc_vs_regular_negative_and_positive['Sentiment Score'], normalize='index')

print(" ")
print("FC Vs. Regular")
print(contigency_pct)

#FIF vs Regular
fif_vs_regular_negative_and_positive= guava_df[(((guava_df['Category']=='FIF') | (guava_df['Category']!='FIF'))) & (((guava_df['Sentiment Score']==-1) | (guava_df['Sentiment Score']==1)))]
fif_vs_regular_negative_and_positive=fif_vs_regular_negative_and_positive[['Category','Sentiment Score']]

fif_vs_regular_negative_and_positive.loc[fif_vs_regular_negative_and_positive['Sentiment Score']== -1, 'Sentiment Score'] = "Negative"
fif_vs_regular_negative_and_positive.loc[fif_vs_regular_negative_and_positive['Sentiment Score']== 1, 'Sentiment Score'] = "Positive"
contigency= pd.crosstab(fif_vs_regular_negative_and_positive['Category'], fif_vs_regular_negative_and_positive['Sentiment Score'])

contigency_pct = pd.crosstab(fif_vs_regular_negative_and_positive['Category'], fif_vs_regular_negative_and_positive['Sentiment Score'], normalize='index')

print(" ")
print("FIF Vs. Regular")
print(contigency_pct)





#Chi-Squared Test-Emotion Vs. Neutral
guava_df.loc[guava_df['Sentiment Score']== -1,'Sentiment Score'] = 1

#FIC vs Regular
fic_vs_regular_emotion_and_neutral= guava_df[(((guava_df['Category']=='FIC') | (guava_df['Category']!='FIC'))) & (((guava_df['Sentiment Score']==0) | (guava_df['Sentiment Score']==1)))]
fic_vs_regular_emotion_and_neutral=fic_vs_regular_emotion_and_neutral[['Category','Sentiment Score']]

fic_vs_regular_emotion_and_neutral.loc[(fic_vs_regular_emotion_and_neutral['Sentiment Score']== 1), 'Sentiment Score'] = "Emotion"
fic_vs_regular_emotion_and_neutral.loc[fic_vs_regular_emotion_and_neutral['Sentiment Score']== 0, 'Sentiment Score'] = "Neutral"
contigency= pd.crosstab(fic_vs_regular_emotion_and_neutral['Category'], fic_vs_regular_emotion_and_neutral['Sentiment Score'])

contigency_pct = pd.crosstab(fic_vs_regular_emotion_and_neutral['Category'], fic_vs_regular_emotion_and_neutral['Sentiment Score'], normalize='index')

print(" ")
print("Emotion Vs. Neutral")
print("FIC Vs. Regular")
print(contigency_pct)

#pFIC vs Regular
pfic_vs_regular_emotion_and_neutral= guava_df[(((guava_df['Category']=='pFIC') | (guava_df['Category']!='pFIC'))) & (((guava_df['Sentiment Score']==0) | (guava_df['Sentiment Score']==1)))]
pfic_vs_regular_emotion_and_neutral=pfic_vs_regular_emotion_and_neutral[['Category','Sentiment Score']]

pfic_vs_regular_emotion_and_neutral.loc[(pfic_vs_regular_emotion_and_neutral['Sentiment Score']== 1), 'Sentiment Score'] = "Emotion"
pfic_vs_regular_emotion_and_neutral.loc[pfic_vs_regular_emotion_and_neutral['Sentiment Score']== 0, 'Sentiment Score'] = "Neutral"
contigency= pd.crosstab(pfic_vs_regular_emotion_and_neutral['Category'], pfic_vs_regular_emotion_and_neutral['Sentiment Score'])

contigency_pct = pd.crosstab(pfic_vs_regular_emotion_and_neutral['Category'], pfic_vs_regular_emotion_and_neutral['Sentiment Score'], normalize='index')

print(" ")
print("Emotion Vs. Neutral")
print("pFIC Vs. Regular")
print(contigency_pct)
#
# #FC vs Regular
fc_vs_regular_emotion_and_neutral= guava_df[(((guava_df['Category']=='FC') | (guava_df['Category']!='FC'))) & (((guava_df['Sentiment Score']==0) | (guava_df['Sentiment Score']==1)))]
fc_vs_regular_emotion_and_neutral=fc_vs_regular_emotion_and_neutral[['Category','Sentiment Score']]

fc_vs_regular_emotion_and_neutral.loc[(fc_vs_regular_emotion_and_neutral['Sentiment Score']== 1), 'Sentiment Score'] = "Emotion"
fc_vs_regular_emotion_and_neutral.loc[fc_vs_regular_emotion_and_neutral['Sentiment Score']== 0, 'Sentiment Score'] = "Neutral"
contigency= pd.crosstab(fc_vs_regular_emotion_and_neutral['Category'], fc_vs_regular_emotion_and_neutral['Sentiment Score'])

contigency_pct = pd.crosstab(fc_vs_regular_emotion_and_neutral['Category'], fc_vs_regular_emotion_and_neutral['Sentiment Score'], normalize='index')

print(" ")
print("Emotion Vs. Neutral")
print("FC Vs. Regular")
print(contigency_pct)


 #FIF vs Regular
fif_vs_regular_emotion_and_neutral= guava_df[(((guava_df['Category']=='FIF') | (guava_df['Category']!='FIF'))) & (((guava_df['Sentiment Score']==0) | (guava_df['Sentiment Score']==1)))]
fif_vs_regular_emotion_and_neutral=fif_vs_regular_emotion_and_neutral[['Category','Sentiment Score']]

fif_vs_regular_emotion_and_neutral.loc[(fif_vs_regular_emotion_and_neutral['Sentiment Score']== 1), 'Sentiment Score'] = "Emotion"
fif_vs_regular_emotion_and_neutral.loc[fif_vs_regular_emotion_and_neutral['Sentiment Score']== 0, 'Sentiment Score'] = "Neutral"
contigency= pd.crosstab(fif_vs_regular_emotion_and_neutral['Category'], fif_vs_regular_emotion_and_neutral['Sentiment Score'])

contigency_pct = pd.crosstab(fif_vs_regular_emotion_and_neutral['Category'], fif_vs_regular_emotion_and_neutral['Sentiment Score'], normalize='index')

print(" ")
print("Emotion Vs. Neutral")
print("FIF Vs. Regular")
print(contigency_pct)






