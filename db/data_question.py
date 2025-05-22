import pandas as pd
import numpy as np
survey = pd.read_csv('data/survey_results_public.csv')
question_df = pd.read_csv('database/questions.csv')
questions = question_df['qname'].to_list()

survey = survey[questions]
q_to_answer = dict()
seen_answer = set()
all_answer = []
for ans in questions:
    # Initialize as a set instead of a list
    column = []
    seen_col = set()
    for value in survey[ans].unique():
        if pd.isna(value) or isinstance(value, float) and np.isnan(value):
            continue
        value_str = str(value)
        if ';' not in value_str:
            if value_str not in seen_col:
                column.append(value_str)
                seen_col.add(value_str)
            if value_str not in seen_answer:
                all_answer.append(value_str)
                seen_answer.add(value_str)
        else:
            for split_value in value_str.split(';'):
                if split_value not in seen_col:
                    column.append(split_value)
                    seen_col.add(split_value)
                if split_value not in seen_answer:
                    all_answer.append(split_value)
                    seen_answer.add(split_value)
    q_to_answer[ans] = column

answer_df = pd.DataFrame([
    {'answerid': i + 1, 'answer': answer}
    for i, answer in enumerate(all_answer)
])

changing = []
qid_to_answer = dict()
for qname in q_to_answer.keys():
    answers = q_to_answer[qname]
    changing = [int(answer_df.loc[answer_df['answer'] == ans, 'answerid'].values[0]) for ans in answers]
    qid = question_df.loc[question_df['qname']==qname, 'qid'].values[0]
    qid_to_answer[qid] = changing

qid_to_answer_df = pd.DataFrame([
    {'qid': qid, 'answerid': qid_to_answer[qid]}
    for qid in qid_to_answer.keys()
])
qid_to_answer_df =  qid_to_answer_df.explode('answerid')
answer_df.to_csv('cleaned-data/answer.csv', index=False)
qid_to_answer_df.to_csv('cleaned-data/qid_answerid.csv', index=False)

