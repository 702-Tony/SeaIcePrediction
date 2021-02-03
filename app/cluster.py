# this is where the clustering will take place
# Lets use Hierarchical Clustering to Learn about our Data

from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from pandas import DataFrame
import numpy as np

le = LabelEncoder()


def scale_data(DF_DATASET):
    scaler = StandardScaler()
    scaler.fit(DF_DATASET)
    scaled_data = scaler.transform(DF_DATASET)
    return scaled_data


def encode_labels(DF_DATASET, encode=True):
    # if encode is false, then undo the encoding
    try:
        if not encode:
            # unencode
            DF_DATASET['date'] = le.inverse_transform(DF_DATASET['date'])
        else:  # else encode the labels
            # encode
            le.fit(DF_DATASET['date'])
            DF_DATASET['date'] = le.transform(DF_DATASET['date'])
    except:
        # this means that the average dataframe has been passed in
        # inelegant, but it works...
        if encode == False:
            # unencode
            DF_DATASET['hemisphere'] = le.inverse_transform(DF_DATASET['hemisphere'])
        else:  # else encode the labels
            # encode
            le.fit(DF_DATASET['hemisphere'])
            DF_DATASET['hemisphere'] = le.transform(DF_DATASET['hemisphere'])
    return DF_DATASET


def h_cluster_data(DF_DATASET, n_clusters=None):
    # encode the labels
    DATASET = encode_labels(DF_DATASET, True)
    # Scale the Data
    scaled_data = scale_data(DF_DATASET)
    # instantiate the Clustering Model
    model = AgglomerativeClustering(distance_threshold=0, n_clusters=n_clusters)
    # Fit and transform the data
    clusters = model.fit_predict(scaled_data)
    DF_DATASET['cluster'] = clusters
    DF_DATASET = encode_labels(DF_DATASET, False)
    return DF_DATASET


def k_cluster_data(DF_DATASET, n_clusters=None):
    # encode the labels
    DATASET = encode_labels(DF_DATASET, True)
    # Scale the Data
    scaled_data = scale_data(DF_DATASET)
    # instantiate the Clustering Model
    model = KMeans(n_clusters=n_clusters)
    # fit and store the predictions
    clusters = model.fit_predict(scaled_data)
    # add a new column with the cluster values
    DF_DATASET['cluster'] = clusters
    # un encode the labels on the Dataframe
    DF_DATASET = encode_labels(DF_DATASET, False)
    return DF_DATASET, model


def k_cluster_data2(DF_DATASET, n_clusters=None):
    # lets prep the list
    year_list_n = {}
    year_list_s = {}
    # this puts each year into its own list in the year_list dict
    for year in range(1979, 2018):
        item = DF_DATASET[DF_DATASET['year'] == year]
        # This adds a dict inside of the year val
        year_list_n[year] = {}
        year_list_s[year] = {}
        # then adds the values to the dict
        # counts up to 366(for leap years...)
        for dayofyear in range(1, 367):
            n_it = item[item['dayofyear'] == dayofyear]
            # empty vals for use in try statementlater
            s_it_n = None
            n_it_n = None
            try:
                # this will throw an exception if val is None
                n_it_n = n_it['n_extent'].values.item()
            except:
                # so we want to store it as None anyways
                n_it_n = None
            try:
                s_it_n = n_it['s_extent'].values.item()
            except:
                s_it_n = None
            year_list_n[year][dayofyear] = n_it_n
            year_list_s[year][dayofyear] = s_it_n
    # create dataframe objs from dicts
    df_yls = DataFrame(data=year_list_s)
    df_yln = DataFrame(data=year_list_n)
    # transpose vals
    df_yls = df_yls.transpose()
    df_yln = df_yln.transpose()
    # reset the indexes
    df_yln.reset_index(inplace=True)
    df_yls.reset_index(inplace=True)
    # create column name list for new dataframe
    column_names = ['year']
    for i in range(1, 367):
        column_names.append(i)
    # set column names on dataframes
    df_yln.columns = column_names
    df_yls.columns = column_names
    # Now impute the columns
    # This will fill in any NaN vals with the mean value from the column
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    # fills the missing values
    df_yln = imputer.fit_transform(df_yln)
    df_yls = imputer.fit_transform(df_yls)
    # recreate the dataframes
    df_yln = DataFrame(df_yln)
    df_yls = DataFrame(df_yls)
    # reset the column names
    df_yln.columns = column_names
    df_yls.columns = column_names
    # Now for the Kmeans for the north...
    kmean_n = KMeans(n_clusters=n_clusters)
    kmean_n.fit(df_yln)
    clusters = kmean_n.predict(df_yln)
    df_yln['clusters'] = clusters
    # ...and for the south
    kmean_s = KMeans(n_clusters=n_clusters)
    kmean_s.fit(df_yls)
    clusters = kmean_s.predict(df_yls)
    df_yls['clusters'] = clusters
    # return both data frames with clusters as well as kmeans
    return df_yln, df_yls, kmean_n, kmean_s
