import random
import pandas as pd
import numpy as np

import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve
from sklearn.preprocessing import MinMaxScaler


class implicit_als(object):
    
    def __init__(self, data):
        data = data.dropna()

        # Convert artists names into numerical IDs
        data['user_id'] = data['user'].astype("category").cat.codes
        data['artist_id'] = data['artist'].astype("category").cat.codes

        # Create a lookup frame so we can get the artist names back in 
        # readable form later.
        self.item_lookup = data[['artist_id', 'artist']].drop_duplicates()
        self.item_lookup['artist_id'] = self.item_lookup.artist_id.astype(str)

        data = data.drop(['user', 'artist'], axis=1)

        # Drop any rows that have 0 plays
        data = data.loc[data.plays != 0]

        self.data=data

        # Create lists of all users, artists and plays
        self.users = list(np.sort(self.data.user_id.unique()))
        self.artists = list(np.sort(self.data.artist_id.unique()))
        self.plays = list(self.data.plays)

        # Get the rows and columns for our new matrix
        self.rows = self.data.user_id.astype(int)
        self.cols = self.data.artist_id.astype(int)

        # Contruct a sparse matrix for our users and items containing number of plays
        self.data_sparse = sparse.csr_matrix((self.plays, (self.rows, self.cols)), shape=(len(self.users), len(self.artists)))


    def train_model(self, alpha_val=40, iterations=10, lambda_val=0.1, features=10):
 
        """ Implementation of Alternating Least Squares with implicit data. We iteratively
            compute the user (x_u) and item (y_i) vectors using the following formulas:

            x_u = ((Y.T*Y + Y.T*(Cu - I) * Y) + lambda*I)^-1 * (X.T * Cu * p(u))
            y_i = ((X.T*X + X.T*(Ci - I) * X) + lambda*I)^-1 * (Y.T * Ci * p(i))

            Args:
                sparse_data (csr_matrix): Our sparse user-by-item matrix

                alpha_val (int): The rate in which we'll increase our confidence
                in a preference with more interactions.

                iterations (int): How many times we alternate between fixing and 
                updating our user and item vectors

                lambda_val (float): Regularization value

                features (int): How many latent features we want to compute.

            Returns:     
                X (csr_matrix): user vectors of size users-by-features

                Y (csr_matrix): item vectors of size items-by-features
            """

        # Calculate the foncidence for each value in our data
        confidence = self.data_sparse * alpha_val #c=1+alpha*r
        
        # Get the size of user rows and item columns
        user_size, item_size = self.data_sparse.shape
        
        # We create the user vectors X of size users-by-features, the item vectors
        # Y of size items-by-features and randomly assign the values.
        self.X = sparse.csr_matrix(np.random.normal(size = (user_size, features)))
        self.Y = sparse.csr_matrix(np.random.normal(size = (item_size, features)))
        
        #Precompute I and lambda * I
        X_I = sparse.eye(user_size) #n*1
        Y_I = sparse.eye(item_size) #m*1
        
        I = sparse.eye(features) #f*1
        lI = lambda_val * I 
        
        # Start main loop. For each iteration we first compute X and then Y
        for i in range(iterations): #学习次数
            print ('iteration %d of %d' % (i+1, iterations))
            
            # Precompute Y-transpose-Y and X-transpose-X
            yTy = self.Y.T.dot(self.Y) #Y(T)Y
            xTx = self.X.T.dot(self.X) #X(T)X

            # Loop through all users
            for u in range(user_size): #对user循环

                # Get the user row.
                u_row = confidence[u,:].toarray() 

                # Calculate the binary preference p(u)
                p_u = u_row.copy()
                p_u[p_u != 0] = 1.0 #建立pu

                # Calculate Cu and Cu - I
                CuI = sparse.diags(u_row, [0])
                Cu = CuI + Y_I

                # Put it all together and compute the final formula
                yT_CuI_y = self.Y.T.dot(CuI).dot(self.Y) #Y(T)(C-I)Y
                yT_Cu_pu = self.Y.T.dot(Cu).dot(p_u.T) #Y(T)CP(T)
                self.X[u] = spsolve(yTy + yT_CuI_y + lI, yT_Cu_pu)

        
            for i in range(item_size):

                # Get the item column and transpose it.
                i_row = confidence[:,i].T.toarray()

                # Calculate the binary preference p(i)
                p_i = i_row.copy()
                p_i[p_i != 0] = 1.0

                # Calculate Ci and Ci - I
                CiI = sparse.diags(i_row, [0])
                Ci = CiI + X_I

                # Put it all together and compute the final formula
                xT_CiI_x = self.X.T.dot(CiI).dot(self.X)
                xT_Ci_pi = self.X.T.dot(Ci).dot(p_i.T)
                self.Y[i] = spsolve(xTx + xT_CiI_x + lI, xT_Ci_pi)
                
        return

    def recommend(self, user_id,  num_items=100):
        """Recommend items for a given user given a trained model
        
        Args:
            user_id (int): The id of the user we want to create recommendations for.
            
            data_sparse (csr_matrix): Our original training data.
            
            user_vecs (csr_matrix): The trained user x features vectors
            
            item_vecs (csr_matrix): The trained item x features vectors
            
            item_lookup (pandas.DataFrame): Used to map artist ids to artist names
            
            num_items (int): How many recommendations we want to return:
            
        Returns:
            recommendations (pandas.DataFrame): DataFrame with num_items artist names and scores
        
        """
        user_vecs=self.X
        item_vecs=self.Y
    
        # Get all interactions by the user
        user_interactions = self.data_sparse[user_id,:].toarray()

        # We don't want to recommend items the user has consumed. So let's
        # set them all to 0 and the unknowns to 1.
        user_interactions = user_interactions.reshape(-1) + 1 #Reshape to turn into 1D array
        user_interactions[user_interactions > 1] = 0 #已经拥有的取0

        # This is where we calculate the recommendation by taking the 
        # dot-product of the user vectors with the item vectors.
        rec_vector = user_vecs[user_id,:].dot(item_vecs.T).toarray()

        # Let's scale our scores between 0 and 1 to make it all easier to interpret.
        min_max = MinMaxScaler()
        rec_vector_scaled = min_max.fit_transform(rec_vector.reshape(-1,1))[:,0] #转成一列
        recommend_vector = user_interactions*rec_vector_scaled
    
        # Get all the artist indices in order of recommendations (descending) and
        # select only the top "num_items" items. 
        item_idx = np.argsort(recommend_vector)[::-1][:num_items]

        artists = []
        scores = []

        # Loop through our recommended artist indicies and look up the actial artist name
        for idx in item_idx:
            artists.append(self.item_lookup.artist.loc[self.item_lookup.artist_id == str(idx)].iloc[0])
            scores.append(recommend_vector[idx])

        # Create a new dataframe with recommended artist names and scores
        recommendations = pd.DataFrame({'artist': artists, 'score': scores})
        
        return recommendations