import pandas as pd
import numpy as np


survey = pd.read_csv('data/survey_results_public.csv')
survey = survey.iloc[:10000]
question_df = pd.read_csv('database/questions.csv')
id_answer = pd.read_csv('database/answer.csv')

basic_questions = question_df.loc[question_df['GID']=='QID1', 'qname'].to_list()
basic_questions.insert(0, 'ResponseId')
basic_info = survey[basic_questions]
basic_info.to_csv('cleaned-data/respondent.csv', index=False)

questions = question_df.loc[question_df['GID']!='QID1', 'qname'].to_list()
questions.insert(0, 'ResponseId')

responses = survey[questions]
explode_columns = []
questions.remove('ResponseId')
for question in questions:
    for value in survey[question].unique():
        value_str = str(value)
        if ';' in value_str:
            responses.loc[:, question] = responses[question].str.split(';')
            explode_columns.append(question)
            break

response_dict = []

for question in questions:
    if question not in explode_columns:
        temp_df = responses[['ResponseId', question]].dropna()
        for row in temp_df.itertuples():
            answer_val = row[2]  # row[1] is index, row[2] is the question column
            answerid_series = id_answer.loc[id_answer['answer'] == answer_val, 'answerid']
            if not answerid_series.empty:
                response_dict.append({
                    'ResponseId': row.ResponseId,
                    'answerid': answerid_series.values[0],
                    'qid': question_df.loc[question_df['qname'] == question, 'qid'].values[0]
                })
    else:
        temp_df = responses[['ResponseId', question]].dropna().copy()
        temp_df[question] = temp_df[question].apply(lambda x: x if isinstance(x, list) else str(x).split(';'))
        temp_df = temp_df.explode(question)

        for row in temp_df.itertuples():
            answer_val = row[2]
            answerid_series = id_answer.loc[id_answer['answer'] == answer_val, 'answerid']
            if not answerid_series.empty:
                response_dict.append({
                    'ResponseId': row.ResponseId,
                    'answerid': answerid_series.values[0],
                    'qid': question_df.loc[question_df['qname'] == question, 'qid'].values[0]
                })

pd.DataFrame(response_dict).to_csv('cleaned-data/responses.csv', index=False)