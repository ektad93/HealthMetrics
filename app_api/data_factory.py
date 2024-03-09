import pandas as pd

def get_data(name, input_date):
    """
        load medical data based on name and input
    """
    data_df = pd.read_csv("data.csv")
    result_df = data_df[(data_df['Name'] == name) &
                        (data_df['Date of Birth'] == input_date)].copy()
    dict_list = result_df.to_dict(orient='records')
    return dict_list
