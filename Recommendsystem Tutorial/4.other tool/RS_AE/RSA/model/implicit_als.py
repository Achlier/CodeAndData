import sys

sys.path.append("RSA/")
from RSA import run_func
import numpy as np
import pandas as pd
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve
from sklearn.preprocessing import MinMaxScaler


class Implicit_als:
    """
    docstring for Implicit_als
    implement the Implicit_als
    """

    def __init__(self, factors=10):
        self.factors = 10

    def init_model(self, rs, dataset_name = 'als' ,alpha_val = 40 ,iterations = 10 ,lambda_val = 0.1 ,features = 10):
        rs.config.dataset_name = dataset_name
        rs.alpha_val = alpha_val
        rs.iterations = iterations
        rs.lambda_val = lambda_val
        rs.features = features
        rs.read_click(rs)

        data = rs.cg.train_df.dropna()
        data.columns = ['user', 'artist', 'plays']
        # Convert artists names into numerical IDs
        data['user_id'] = data['user'].astype("category").cat.codes
        data['artist_id'] = data['artist'].astype("category").cat.codes

        # Create a lookup frame so we can get the artist names back in
        # readable form later.
        rs.item_lookup = data[['artist_id', 'artist']].drop_duplicates()
        rs.item_lookup['artist_id'] = rs.item_lookup.artist_id.astype(str)

        data = data.drop(['user', 'artist'], axis=1)

        # Drop any rows that have 0 plays
        data = data.loc[data.plays != 0]

        rs.data = data

        # Create lists of all users, artists and plays
        rs.users = list(np.sort(rs.data.user_id.unique()))
        rs.artists = list(np.sort(rs.data.artist_id.unique()))
        rs.plays = list(rs.data.plays)

        # Get the rows and columns for our new matrix
        rs.rows = rs.data.user_id.astype(int)
        rs.cols = rs.data.artist_id.astype(int)

        # Contruct a sparse matrix for our users and items containing number of plays
        rs.data_sparse = sparse.csr_matrix((rs.plays, (rs.rows, rs.cols)), shape=(len(rs.users), len(rs.artists)))

    def train_model(self, rs):

        # Calculate the foncidence for each value in our data
        confidence = rs.data_sparse * rs.alpha_val  # c=1+alpha*r

        # Get the size of user rows and item columns
        user_size, item_size = rs.data_sparse.shape

        # We create the user vectors X of size users-by-rs.features, the item vectors
        # Y of size items-by-rs.features and randomly assign the values.
        rs.X = sparse.csr_matrix(np.random.normal(size=(user_size, rs.features)))
        rs.Y = sparse.csr_matrix(np.random.normal(size=(item_size, rs.features)))

        # Precompute I and lambda * I
        X_I = sparse.eye(user_size)  # n*1
        Y_I = sparse.eye(item_size)  # m*1

        I = sparse.eye(rs.features)  # f*1
        lI = rs.lambda_val * I

        # Start main loop. For each iteration we first compute X and then Y
        for i in range(rs.iterations):  # 学习次数
            print('iteration %d of %d' % (i + 1, rs.iterations))

            # Precompute Y-transpose-Y and X-transpose-X
            yTy = rs.Y.T.dot(rs.Y)  # Y(T)Y
            xTx = rs.X.T.dot(rs.X)  # X(T)X

            # Loop through all users
            for u in range(user_size):  # 对user循环

                # Get the user row.
                u_row = confidence[u, :].toarray()

                # Calculate the binary preference p(u)
                p_u = u_row.copy()
                p_u[p_u != 0] = 1.0  # 建立pu

                # Calculate Cu and Cu - I
                CuI = sparse.diags(u_row, [0])
                Cu = CuI + Y_I

                # Put it all together and compute the final formula
                yT_CuI_y = rs.Y.T.dot(CuI).dot(rs.Y)  # Y(T)(C-I)Y
                yT_Cu_pu = rs.Y.T.dot(Cu).dot(p_u.T)  # Y(T)CP(T)
                rs.X[u] = spsolve(yTy + yT_CuI_y + lI, yT_Cu_pu)

            for i in range(item_size):
                # Get the item column and transpose it.
                i_row = confidence[:, i].T.toarray()

                # Calculate the binary preference p(i)
                p_i = i_row.copy()
                p_i[p_i != 0] = 1.0

                # Calculate Ci and Ci - I
                CiI = sparse.diags(i_row, [0])
                Ci = CiI + X_I

                # Put it all together and compute the final formula
                xT_CiI_x = rs.X.T.dot(CiI).dot(rs.X)
                xT_Ci_pi = rs.X.T.dot(Ci).dot(p_i.T)
                rs.Y[i] = spsolve(xTx + xT_CiI_x + lI, xT_Ci_pi)

    def predict(self, rs):
        pass

    def recommend(self, rs, user_id, num_items=10):
        user_vecs = rs.X
        item_vecs = rs.Y

        # Get all interactions by the user
        user_interactions = rs.data_sparse[user_id, :].toarray()

        # We don't want to recommend items the user has consumed. So let's
        # set them all to 0 and the unknowns to 1.
        user_interactions = user_interactions.reshape(-1) + 1  # Reshape to turn into 1D array
        user_interactions[user_interactions > 1] = 0  # 已经拥有的取0

        # This is where we calculate the recommendation by taking the
        # dot-product of the user vectors with the item vectors.
        rec_vector = user_vecs[user_id, :].dot(item_vecs.T).toarray()

        # Let's scale our scores between 0 and 1 to make it all easier to interpret.
        min_max = MinMaxScaler()
        rec_vector_scaled = min_max.fit_transform(rec_vector.reshape(-1, 1))[:, 0]  # 转成一列
        recommend_vector = user_interactions * rec_vector_scaled

        # Get all the artist indices in order of recommendations (descending) and
        # select only the top "num_items" items.
        item_idx = np.argsort(recommend_vector)[::-1][:num_items]

        artists = []
        scores = []

        # Loop through our recommended artist indicies and look up the actial artist name
        for idx in item_idx:
            artists.append(rs.item_lookup.artist.loc[rs.item_lookup.artist_id == str(idx)].iloc[0])
            scores.append(recommend_vector[idx])

        # Create a new dataframe with recommended artist names and scores
        recommendations = pd.DataFrame({'artist': artists, 'score': scores})

        return recommendations