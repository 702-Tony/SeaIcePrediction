# this is where the clustering will take place
# Lets use Hierarchical Clustering to Learn about our Data

from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
def scale_data(DF_DATASET):
    scaler = StandardScaler()
    scaler.fit(DF_DATASET)
    scaled_data = scaler.transform(DF_DATASET)
    return scaled_data
def encode_labels(DF_DATASET, encode=True):
    # if encode is false, then undo the encoding
    if encode == False:
        # unencode
        DF_DATASET['date'] = le.inverse_transform(DF_DATASET['date'])
    else : # else encode the labels
        # encode
        le.fit(DF_DATASET['date'])
        DF_DATASET['date'] = le.transform(DF_DATASET['date'])
    # print('After','##########'*5)
    # print(DF_DATASET.head())
    return DF_DATASET

def h_cluster_data(DF_DATASET, n_clusters=None):
    # encode the labels
    DATASET = encode_labels(DF_DATASET, True)
    # Scale the Data
    scaled_data = scale_data(DF_DATASET)
    # instantiate the Clustering Model
    model = AgglomerativeClustering(distance_threshold=0, n_clusters = n_clusters)
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
