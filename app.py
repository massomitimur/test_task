from flask import Flask, request, jsonify
import pandas as pd

df = pd.read_csv('salary_survey.csv')
# Rename the most frequently used columns for the convenience
df = df.rename(columns={
    'Timestamp': 'timestamp',
    'Employment Type': 'employment_type',
    'Company Name': 'company_name',
    'Company Size - # Employees': 'company_size',
    'Primary Location (Country)': 'country',
    'Primary Location (City)': 'city',
    'Industry in Company': 'industry',
    'Public or Private Company': 'public_or_private',
    'Years Experience in Industry': 'experience_in_industry',
    'Years of Experience in Current Company': 'experience_in_company',
    'Highest Level of Formal Education Completed': 'education',
    'Total Base Salary in 2018 (in USD)': 'salary',
    'Gender': 'gender'
})

def filter_data(filter_criteria, sort_criteria, fields):

    resulting_df = df 

    # filter
    for column, value in filter_criteria.items():
        resulting_df = resulting_df[resulting_df[column] == value]
    # sort
    if sort_criteria:
        resulting_df = resulting_df.sort_values(by=sort_criteria)
    # leave selected columns
    if fields:
        resulting_df = resulting_df[fields]

    return resulting_df.to_dict(orient='records')


app = Flask('app')

@app.route('/api/compensation_data', methods=['GET'])
def filter_compensation_data():

    query_parameters = request.args

    filter_fields =  df.columns.tolist()
    filter_criteria = {}
    sort_criteria = []
    fields = []

    for parameter_name in query_parameters:
        if parameter_name in filter_fields:
            if parameter_name == 'salary':
                filter_criteria[parameter_name] = int(query_parameters.get(parameter_name))
            else:
                filter_criteria[parameter_name] = query_parameters.get(parameter_name)
        if parameter_name == 'sort' and query_parameters.get(parameter_name) in filter_fields:
            sort_criteria.append(query_parameters.get(parameter_name))
        if parameter_name == 'fields':
            for field in  query_parameters.get(parameter_name).split(','):
                if field in filter_fields:
                    fields.append(field)

    resulting_data = filter_data(filter_criteria, sort_criteria, fields)  

    return jsonify(resulting_data)



if __name__ == '__main__':
    app.run()

