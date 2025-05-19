import pandas as pd

if __name__ == "__main__":
    survey = pd.read_csv('data/survey_results_public.csv')
    schema = pd.read_csv('data/survey_results_schema.csv')

    survey_cols = survey.columns
    schema_qname = schema['qname']
    exclude_in_sim = ['OrgSize', 'PurchaseInfluence', 'BuyNewTool', 'BuildvsBuy', 
                    'TechEndorse', 'SurveyLength', 'SurveyEase', 'Industry', 'Check',
                    'Knowledge_1', 'Knowledge_2', 'Knowledge_3', 'Knowledge_4',
                    'Knowledge_5', 'Knowledge_6', 'Knowledge_7', 'Knowledge_8',
                    'Knowledge_9', 'Frequency_1', 'Frequency_2', 'Frequency_3']
    similar_schema = [col for col in schema_qname if col in survey_cols and col not in exclude_in_sim]

    exclude_in_survey = ['ResponseId', 'EmbeddedHaveWorkedWith', 'EmbeddedWantToWorkWith', 'EmbeddedAdmired', 
                        'MiscTechHaveWorkedWith', 'MiscTechWantToWorkWith', 'MiscTechAdmired',
                        'NEWCollabToolsHaveWorkedWith', 'NEWCollabToolsWantToWorkWith', 'NEWCollabToolsAdmired',
                        ]
    include_survey = [col for col in survey_cols if col not in similar_schema and col not in exclude_in_sim and col not in exclude_in_survey]
    #include survey fields need to be added to schema with qid, qname, ...
    fields = {'schema': similar_schema, 'survey':include_survey}

    #TODO: handle field in survey that dont have qid, create groupquestion, do at least 2NF tonight
    