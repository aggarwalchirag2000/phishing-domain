import pandas as pd
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class Prediction:
    def __init__(self,filename):
        self.filename = filename
        self.location = './predict_uploads/'+ self.filename
    def predict_data(self):
        try:
            x = pd.read_csv(self.location)
            df = x.copy()
            knn_file = './models/kmean.sav'
            knn_file_model = pickle.load(open(knn_file,'rb'))

            df['cluster'] = knn_file_model.predict(x)

            scaler_file = './models/scaler.sav'
            scaler_model = pickle.load(open(scaler_file, 'rb'))

            x_scaled = pd.DataFrame(scaler_model.transform(x),columns = x.columns)
            x_scaled['cluster'] = df['cluster']
            y = []
            # for i in set(x_scaled['cluster']):
            for i in range(0,1):
                x_cluster = x_scaled.iloc[np.where(x_scaled['cluster'] == i)]
                x_final = x_cluster.drop(columns = 'cluster')

                pca_file = './models/pca'+str(i)+'.sav'

                pca_model = pickle.load(open(pca_file,'rb'))
                x_pca = pca_model.transform(x_final)
                x_pca_len = len(x_pca[0]) + 1
                x_pca = pd.DataFrame(x_pca, columns=['PC' + str(i) for i in range(1, x_pca_len)])

                rf_file = 'RandomForest' + str(i) + '.sav'
                rf_model = pickle.load(open(rf_file, 'rb'))



            # return knn_file_model




        except Exception as e:
            print("exception prediction")
            raise Exception