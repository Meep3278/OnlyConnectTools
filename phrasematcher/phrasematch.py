from datamuse import Datamuse
import pandas as pd

def getData(filename):
    input = open(filename, "r") 
    data = input.read()
    data_into_list = data.replace('\n', ' ').split(", ")
    return data_into_list

def dm_to_df(datamuse_response):
    """Converts the json response of the datamuse API into a DataFrame
    :datamuse_response
        [{'word': 'foo', 'score': 100}, {'word': 'bar', 'score': 120}]
    """
    reformatted = {
        'word': [response['word'] for response in datamuse_response],
        'score': [response['score'] for response in datamuse_response]
    }
    return pd.DataFrame.from_dict(reformatted)

def list_to_df(input):
    dfbefore = pd.DataFrame(columns=['word', 'score', 'ogword'])
    dfafter = pd.DataFrame(columns=['word', 'score', 'ogword'])
    for word in input:
        print(word)
        phrasesbefore = api.words(rel_jja=word, max=200)
        phrasesafter = api.words(rel_jjb=word, max=200)
        dfbeforenew = dm_to_df(phrasesbefore)
        dfafternew = dm_to_df(phrasesafter)
        dfbeforenew["ogword"] = word
        dfafternew["ogword"] = word
        dfbefore = pd.concat([dfbefore, dfbeforenew])
        dfafter = pd.concat([dfafter, dfafternew])
    return dfbefore, dfafter

input1 = getData("input1.txt")
# input2 = getData("input2.txt")
input2 = ['god']

api = Datamuse()

df1before, df1after = list_to_df(input1)
df2before, df2after = list_to_df(input2)
commonlist = getData("commonwords.txt")
commondf = pd.DataFrame({'word':commonlist})

dfbefore = pd.merge(df1before, df2before, on='word', how='inner')
dfbefore["place"] = 'before'

dfafter = pd.merge(df1after, df2after, on='word', how='inner')
dfafter["place"] = 'after'

df = pd.concat([dfbefore, dfafter])
mask = df.word.isin(commondf.word)
df = df[~mask]
sorted_indices = (df["score_x"] + df["score_y"]).sort_values().index
df = df.loc[sorted_indices, :]
print(df.head(50))