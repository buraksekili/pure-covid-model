print("Importing modules", flush = True)
import pandas as pd
import numpy as np
from joblib import load
from sklearn.linear_model import LogisticRegression
from datetime import datetime,timedelta

def add_from_person_table(concept_id, column_name, new_column_name, df):
    sub_table = df[df[column_name] == concept_id]
    tmp_arr = np.zeros(df.shape[0])
    for person_id in sub_table.person_id.values:
        index = df[df.person_id == person_id].index[0]
        tmp_arr[index] = 1
    
    df[new_column_name] = tmp_arr
    return df

visit_table = pd.read_csv('/data/visit_occurrence.csv', usecols=['person_id', 'visit_concept_id'])
def add_visit_type(visit_concept_id, column_name, df):
    illness_table = visit_table[visit_table.visit_concept_id == visit_concept_id]
    tmp_arr = np.zeros(df.shape[0])
    for person_id in illness_table.person_id.values:
        index = df[df.person_id == person_id].index[0]
        tmp_arr[index] = 1
    df[column_name] = tmp_arr

    return df

def getFirstPcrDate(measurements):
    
    df=measurements.loc[measurements['measurement_concept_id'] == 706163]
    df=df.sort_values(by='measurement_date') 
    pcr_date_string = df['measurement_date'].iloc[0]
    
    pcr_date_object = datetime.strptime(pcr_date_string, '%Y-%m-%d')
    pcr_before = pcr_date_object - timedelta(7) 
    
    return pcr_before

def filterByPcrDate(table_name,column_name,filter_date):
    return table_name[table_name[column_name] >= str(filter_date)].sort_values(by=column_name)

measurements_table = pd.read_csv('/data/measurement.csv', usecols=['person_id', 'measurement_concept_id', 'measurement_date','value_as_number'])
firstPcrDate=getFirstPcrDate(measurements_table)
measurements_table=filterByPcrDate(measurements_table,'measurement_date',firstPcrDate)
measurements_table = measurements_table.drop('measurement_date', 1)
measurements_table.dropna(subset = ["value_as_number"], inplace=True)

def add_measurements(concept_id, column_name, df):
    selected_measurement = measurements_table[measurements_table.measurement_concept_id == concept_id]
    tmp_median = np.zeros(df.shape[0])
   
    for person_id in np.unique(selected_measurement.person_id.values):
        try:
            index = df[df.person_id == person_id].index[0]
            measurement_values = selected_measurement[selected_measurement.person_id == person_id].value_as_number.values
            
            median_val = np.median(measurement_values)
            tmp_median[index] = median_val
        except:
            pass
        
    df[column_name + '_median'] = tmp_median

    return df

def add_all_measurements(df):
    measurements_concept_id_arr = np.unique(measurements_table.measurement_concept_id.values)
    # measurements_concept_id_arr = measurements_table['measurement_concept_id'].value_counts()[:50].index.tolist()
    for measurement_concept_id in measurements_concept_id_arr:
        add_measurements(measurement_concept_id, 'measurement_' + str(measurement_concept_id), df)

condition_table = pd.read_csv('/data/condition_occurrence.csv', usecols=['person_id', 'condition_concept_id', 'condition_start_date'])
condition_table=filterByPcrDate(condition_table,'condition_start_date',firstPcrDate)
def add_conditions(df):
    person_id_arr = df.person_id.values
    
    tmp_arr_fever = np.zeros(df.shape[0])
    tmp_arr_cough = np.zeros(df.shape[0])
    tmp_arr_soreThroat = np.zeros(df.shape[0])
    tmp_arr_sputum = np.zeros(df.shape[0])
    tmp_arr_dyspnea = np.zeros(df.shape[0])
    tmp_arr_chest_pain = np.zeros(df.shape[0])
    tmp_arr_fatigue = np.zeros(df.shape[0])
    tmp_arr_diarrhea = np.zeros(df.shape[0])
    tmp_arr_headache = np.zeros(df.shape[0])
    tmp_arr_backache = np.zeros(df.shape[0])
    tmp_arr_smell_taste = np.zeros(df.shape[0])

    for person_id in person_id_arr:
        person_conditions_df = condition_table[condition_table.person_id == person_id]
        unique_person_condition_list = np.unique(person_conditions_df.condition_concept_id.values)
        
        index = df[df.person_id == person_id].index[0]
        
        if (437663 in unique_person_condition_list):
            tmp_arr_fever[index] = 1
        else:
            tmp_arr_fever[index] = 0
        
        if (254761 in unique_person_condition_list):
            tmp_arr_cough[index] = 1
        else:
            tmp_arr_cough[index] = 0
            
        if (28060 in unique_person_condition_list):
            tmp_arr_soreThroat[index] = 1
        else:
            tmp_arr_soreThroat[index] = 0            
            
        if (433596 in unique_person_condition_list):
            tmp_arr_sputum[index] = 1
        else:
            tmp_arr_sputum[index] = 0
            
        if (312437 in unique_person_condition_list):
            tmp_arr_dyspnea[index] = 1
        else: 
            tmp_arr_dyspnea[index] = 0
            
        if (77670 in unique_person_condition_list):
            tmp_arr_chest_pain[index] = 1
        else: 
            tmp_arr_chest_pain[index] = 0

        if (4223659 in unique_person_condition_list):
            tmp_arr_fatigue[index] = 1
        else:
            tmp_arr_fatigue[index] = 0
            
        if (196523 in unique_person_condition_list):
            tmp_arr_diarrhea[index] = 1
        else:
            tmp_arr_diarrhea[index] = 0
            
        if (378253 in unique_person_condition_list):
            tmp_arr_headache[index] = 1
        else:
            tmp_arr_headache[index] = 0
        if (134736 in unique_person_condition_list):
            tmp_arr_backache[index] = 1
        else: 
            tmp_arr_backache[index] = 0
        if (43530714 in unique_person_condition_list or 436235 in unique_person_condition_list or 4185711 in unique_person_condition_list):
            tmp_arr_smell_taste[index] = 1
        else:
            tmp_arr_smell_taste[index] = 0

    
    df['fever'] = tmp_arr_fever
    df['cough'] = tmp_arr_cough
    df['soreThroat'] = tmp_arr_soreThroat
    df['sputum'] = tmp_arr_sputum
    df['dyspnea'] = tmp_arr_dyspnea
    df['chest_pain'] = tmp_arr_chest_pain
    df['fatigue'] = tmp_arr_fatigue
    df['diarrhea'] = tmp_arr_diarrhea
    df['headache'] = tmp_arr_headache
    df['backache'] = tmp_arr_backache   
    df['smell_taste'] = tmp_arr_smell_taste

        
    return df

person_table = pd.read_csv('/data/person.csv', usecols=['person_id', 'year_of_birth', 'gender_concept_id', 'race_concept_id'])
person_table = person_table.sort_values(by=['person_id'])

print("Adding Age")
ages = 2020 - person_table.year_of_birth
person_table['age'] = ages
person_table.drop(['year_of_birth'], axis=1, inplace=True)
person_table.age = person_table.age.map(lambda a: 1 if a > 60 else 0)

person_table = add_from_person_table(8507, 'gender_concept_id', 'male', person_table)
person_table = add_from_person_table(8532, 'gender_concept_id', 'female', person_table)
person_table.drop(['gender_concept_id'], axis=1, inplace=True)

person_table = add_from_person_table(8515, 'race_concept_id', 'asian', person_table)
person_table = add_from_person_table(8527, 'race_concept_id', 'white', person_table)
person_table = add_from_person_table(8516, 'race_concept_id', 'black', person_table)
person_table.drop(['race_concept_id'], axis=1, inplace=True)

person_table = add_visit_type(32037, 'intensive_care', person_table)
person_table = add_visit_type(9203, 'emergency_room', person_table)
person_table = add_visit_type(9201, 'inpatient', person_table)

device_exposure = pd.read_csv('/data/device_exposure.csv', usecols=['person_id', 'device_concept_id'])
tmp_arr = np.zeros(person_table.shape[0])
for person_id in device_exposure.person_id.values:
    index = person_table[person_table.person_id == person_id].index[0]
    tmp_arr[index] = 1
    
person_table['ventilator'] = tmp_arr

observation_table = pd.read_csv('/data/observation.csv', usecols=['person_id', 'observation_concept_id', 'value_as_string'])
tobacco_table = observation_table[(observation_table.observation_concept_id == 4005823) & (observation_table.value_as_string == 'Yes')]
tmp_arr = np.zeros(person_table.shape[0])
for person_id in tobacco_table.person_id.values:
    index = person_table[person_table.person_id == person_id].index[0]
    tmp_arr[index] = 1
person_table['tobacco'] = tmp_arr


person_table = add_measurements(3024561, 'Albumin' ,person_table)
person_table = add_measurements(3006923, 'ALT' ,person_table)
person_table = add_measurements(3013721, 'AST' ,person_table)
person_table = add_measurements(3016723, 'Creatinine' ,person_table)
person_table = add_measurements(3010156, 'CRP' ,person_table)
person_table = add_measurements(42870366, 'D-dimer' ,person_table)
person_table = add_measurements(3000963, 'Hemoglobin' ,person_table)
person_table = add_measurements(3000905, 'Leukocytes' ,person_table)
person_table = add_measurements(3004327, 'Lymphocytes' ,person_table)
person_table = add_measurements(3013650, 'Neutrophils' ,person_table)
person_table = add_measurements(3023103, 'Potassium' ,person_table)
person_table = add_measurements(3046279, 'Procalcitonin' ,person_table)
person_table = add_measurements(3019550, 'Sodium' ,person_table)
person_table = add_measurements(3022250, 'Lactate Dehydrogenase' ,person_table)

person_table = add_conditions(person_table)


df = person_table.drop(['person_id'], axis=1)
df.columns = df.columns.astype(str)


training_columns = pd.read_csv('/model/training_columns.csv', index_col=0).columns.values
testing_columns = df.columns.values

for test_column in testing_columns:
    if (test_column not in training_columns):
        print(test_column)
        print("Before: ", df.shape)
        df.drop([test_column], axis = 1, inplace=True)
        print("After: ", df.shape)

for training_column in training_columns:
    if (training_column not in testing_columns):
        print(training_column)
        df[training_column] = 0


X = df.values

clf =  load('/model/v6.joblib')
print('clf is loaded')
Y_pred = clf.predict_proba(X)[:,1]
print('prediction is done for xg')

person_id = person_table[['person_id']]

output = pd.DataFrame(Y_pred,columns = ['score'])
output_prob = pd.concat([person_id,output],axis = 1)
output_prob.columns = ["person_id", "score"]
output_prob.to_csv('/output/predictions.csv', index = False)
print("Inferring stage finished", flush = True)