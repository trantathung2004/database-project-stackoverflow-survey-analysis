import pandas as pd
import re

def generate_question_from_qname(qname: str) -> str:
    # Add a space before each capital letter, except the first one
    spaced = re.sub(r'(?<!^)(?=[A-Z])', ' ', qname)
    return f"What is {spaced}?"

if __name__ == "__main__":
    survey = pd.read_csv('data/survey_results_public.csv')
    schema = pd.read_csv('data/survey_results_schema.csv')

    survey_cols = survey.columns
    schema_qname = schema['qname']

    qname_dict = {
    qname: matches
    for qname in schema_qname
    if (matches := [col for col in survey_cols if col.startswith(qname)]) and len(matches) > 1
    }
    # assign 'AITool', 'AISearchDev', 'AIThreat' these to AI
    # 'Basic Information': 
    selected_group = [ 'LearnCode', 'Language', 'Database', 'Platform', 'Webframe', 'OpSys']
    group_table = {'Basic Information': 'QID1'}
    
    for group in selected_group:
        qid = schema.loc[schema['qname']==group, 'qid'].values[0]
        group_table[group] = qid
    group_table['AI'] = 'QID319'
    question_FK = {'Basic Information': ['MainBranch', 'Age', 'Employment', 'EdLevel', 'Country'], 'AI': ['AISelect', 'AIToolCurrently Using', 'AIToolNot interested in Using', 'AIThreat']}
    qnames = ['MainBranch', 'Age', 'Employment', 'EdLevel', 'Country', 'AISelect', 'AIToolCurrently Using', 'AIToolNot interested in Using', 'AIThreat']
    for group in group_table.keys():
        if group not in qname_dict.keys(): continue
        question_FK[group] = qname_dict[group]
        qnames += qname_dict[group]

    qtable = []

    g_table = pd.DataFrame([
    {'gid': qid, 'groupname': groupname}
    for groupname, qid in group_table.items()
])
    g_table.to_csv('cleaned-data/group.csv', index=False)

    rows = []
    id = 0
    for groupname, qname_list in question_FK.items():
        GID = group_table[groupname]
        for qname in qname_list:
            # print(qname in schema['qname'].tolist())
            id += 1
            question_text = schema.loc[schema['qname']==qname, 'question'].values[0] if qname in schema['qname'].tolist() else generate_question_from_qname(qname)
            rows.append({
                'qid': id,
                'qname': qname,
                'question': question_text,
                'GID': GID
            })

    question_table = pd.DataFrame(rows)
    # Optional: Reset index if needed
    # question_table.reset_index(drop=True, inplace=True)
    question_table.to_csv('cleaned-data/questions.csv', index=False) 

