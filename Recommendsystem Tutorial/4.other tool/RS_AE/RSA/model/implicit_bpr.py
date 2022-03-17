import os
import sys
import numpy as np
import pandas as pd
from math import ceil
from tqdm import trange
from subprocess import call
from itertools import islice
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import normalize
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix, dok_matrix
from sklearn.preprocessing import MinMaxScaler


class BPR:
    """
    Bayesian Personalized Ranking (BPR) for implicit feedback data

    Parameters
    ----------
    learning_rate : float, default 0.01
        learning rate for gradient descent

    n_factors : int, default 20
        Number/dimension of user and item latent factors

    n_iters : int, default 15
        Number of iterations to train the algorithm

    batch_size : int, default 1000
        batch size for batch gradient descent, the original paper
        uses stochastic gradient descent (i.e., batch size of 1),
        but this can make the training unstable (very sensitive to
        learning rate)

    reg : int, default 0.01
        Regularization term for the user and item latent factors

    seed : int, default 1234
        Seed for the randomly initialized user, item latent factors

    verbose : bool, default True
        Whether to print progress bar while training

    Attributes
    ----------
    user_factors : 2d ndarray, shape [n_users, n_factors]
        User latent factors learnt

    item_factors : 2d ndarray, shape [n_items, n_factors]
        Item latent factors learnt

    References
    ----------
    S. Rendle, C. Freudenthaler, Z. Gantner, L. Schmidt-Thieme
    Bayesian Personalized Ranking from Implicit Feedback
    - https://arxiv.org/abs/1205.2618
    """
    def __init__(self, factors=10):
        self.factors = 10

    def init_model(self, rs, dataset_name = 'als', learning_rate=0.01, n_factors=15, n_iters=10,
                 batch_size=1000, reg=0.01, seed=1234, verbose=True):
        rs.config.dataset_name = dataset_name
        rs.reg = reg  # 正则系数
        rs.seed = seed  # 随机数
        rs.verbose = verbose  # 进度条bool
        rs.n_iters = n_iters  # 总循环次数
        rs.n_factors = n_factors  # 特征值个数
        rs.batch_size = batch_size  # sample个数
        rs.learning_rate = learning_rate
        rs.read_click(rs)

        items_col = 'item'
        users_col = 'user'
        ratings_col = 'clicks'
        threshold = None
        # to avoid re-computation at predict
        rs._prediction = None

        rs.X, rs.df = create_matrix(rs.cg.train_df, users_col, items_col, ratings_col, threshold)
        rs.X_train, rs.X_test = create_train_test(rs.X, test_size = 0.2, seed = seed)

    def train_model(self, rs):
        """
        Parameters
        ----------
        ratings : scipy sparse csr_matrix, shape [n_users, n_items]
            sparse matrix of user-item interactions
        """
        ratings = rs.X_train
        indptr = ratings.indptr  # 每行元素(非零元素)个数累计结果
        indices = ratings.indices  # 非0元素对应的列索引值所组成数组
        n_users, n_items = ratings.shape

        # ensure batch size makes sense, since the algorithm involves
        # for each step randomly sample a user, thus the batch size
        # should be smaller than the total number of users or else
        # we would be sampling the user with replacement
        batch_size = rs.batch_size
        if n_users < batch_size:  # batch_size 太大，或是用户数太少
            batch_size = n_users
            sys.stderr.write('WARNING: Batch size is greater than number of users,'
                             'switching to a batch size of {}\n'.format(n_users))

        batch_iters = n_users // batch_size  # 内循环次数 向下取整

        # initialize random weights
        rstate = np.random.RandomState(rs.seed)  # 随机Object
        rs.user_factors = rstate.normal(size=(n_users, rs.n_factors))  # user_factors normal matrix
        rs.item_factors = rstate.normal(size=(n_items, rs.n_factors))  # item_factors normal matrix

        # progress bar for training iteration if verbose is turned on
        loop = range(rs.n_iters)  # 总循环
        if rs.verbose:
            loop = trange(rs.n_iters, desc=self.__class__.__name__)  # 进度条

        for _ in loop:
            for _ in range(batch_iters):
                sampled = self._sample(rs, n_users, n_items, indices, indptr)  # sample 获取
                sampled_users, sampled_pos_items, sampled_neg_items = sampled
                self._update(rs, sampled_users, sampled_pos_items, sampled_neg_items)

    def _sample(self, rs, n_users, n_items, indices, indptr):
        """sample batches of random triplets u, i, j"""
        sampled_pos_items = np.zeros(rs.batch_size, dtype=np.int)
        sampled_neg_items = np.zeros(rs.batch_size, dtype=np.int)
        sampled_users = np.random.choice(
            n_users, size=rs.batch_size, replace=False)  # 从n_users 随机选 size个

        for idx, user in enumerate(sampled_users):
            nebor_add = 1
            pos_items = indices[indptr[user]:indptr[user + nebor_add]]  # 当前用户的item_index列表
            while len(pos_items) == 0:
                nebor_add += 1
                pos_items = indices[indptr[user]:indptr[user + nebor_add]]
            pos_item = np.random.choice(pos_items)  # 随机选取item
            neg_item = np.random.choice(n_items)  # 随机选取item
            while neg_item in pos_items:
                neg_item = np.random.choice(n_items)  # 在用户non-positive中随机选取一个为neg

            sampled_pos_items[idx] = pos_item  # 获取sample
            sampled_neg_items[idx] = neg_item  # ..

        return sampled_users, sampled_pos_items, sampled_neg_items

    def _update(self, rs, u, i, j):
        """
        update according to the bootstrapped user u,
        positive item i and negative item j
        """
        user_u = rs.user_factors[u]  # u_factors
        item_i = rs.item_factors[i]  # i_factors
        item_j = rs.item_factors[j]  # j_factors

        # decompose the estimator, compute the difference between
        # the score of the positive items and negative items; a
        # naive implementation might look like the following:
        # r_ui = np.diag(user_u.dot(item_i.T))
        # r_uj = np.diag(user_u.dot(item_j.T))
        # r_uij = r_ui - r_uj

        # however, we can do better, so
        # for batch dot product, instead of doing the dot product
        # then only extract the diagonal element (which is the value
        # of that current batch), we perform a hadamard product,
        # i.e. matrix element-wise product then do a sum along the column will
        # be more efficient since it's less operations
        # http://people.revoledu.com/kardi/tutorial/LinearAlgebra/HadamardProduct.html
        # r_ui = np.sum(user_u * item_i, axis = 1)
        #
        # then we can achieve another speedup by doing the difference
        # on the positive and negative item up front instead of computing
        # r_ui and r_uj separately, these two idea will speed up the operations
        # from 1:14 down to 0.36
        r_uij = np.sum(user_u * (item_i - item_j), axis=1)
        sigmoid = np.exp(-r_uij) / (1.0 + np.exp(-r_uij))

        # repeat the 1 dimension sigmoid n_factors times so
        # the dimension will match when doing the update
        sigmoid_tiled = np.tile(sigmoid, (rs.n_factors, 1)).T  # n维重复输出

        # update using gradient descent
        grad_u = sigmoid_tiled * (item_j - item_i) + rs.reg * user_u
        grad_i = sigmoid_tiled * -user_u + rs.reg * item_i
        grad_j = sigmoid_tiled * user_u + rs.reg * item_j
        rs.user_factors[u] -= rs.learning_rate * grad_u
        rs.item_factors[i] -= rs.learning_rate * grad_i
        rs.item_factors[j] -= rs.learning_rate * grad_j


    def predict(self, rs):
        """
        Obtain the predicted ratings for every users and items
        by doing a dot product of the learnt user and item vectors.
        The result will be cached to avoid re-computing it every time
        we call predict, thus there will only be an overhead the first
        time we call it. Note, ideally you probably don't need to compute
        this as it returns a dense matrix and may take up huge amounts of
        memory for large datasets
        """
        if rs._prediction is None:
            rs._prediction = rs.user_factors.dot(rs.item_factors.T)

        return rs._prediction

    def _predict_user(self, rs, user):
        """
        returns the predicted ratings for the specified user,
        this is mainly used in computing evaluation metric
        """
        user_pred = rs.user_factors[user].dot(rs.item_factors.T)
        return user_pred

    def recommend(self, rs, user_id, num_items=10):
        user_vecs = rs.user_factors
        item_vecs = rs.item_factors

        # Get all interactions by the user
        user_interactions = rs.X_train[user_id, :].toarray()

        # We don't want to recommend items the user has consumed. So let's
        # set them all to 0 and the unknowns to 1.
        user_interactions = user_interactions.reshape(-1) + 1  # Reshape to turn into 1D array
        user_interactions[user_interactions > 1] = 0  # 已经拥有的取0

        # This is where we calculate the recommendation by taking the
        # dot-product of the user vectors with the item vectors.
        rec_vector = user_vecs[user_id, :].dot(item_vecs.T)

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
            artists.append(idx)
            scores.append(recommend_vector[idx])

        # Create a new dataframe with recommended artist names and scores
        recommendations = pd.DataFrame({'artist': artists, 'score': scores})

        return recommendations

    def _recommend_user(self, rs, user, N):
        """the top-N ranked items for a given user"""
        scores = self._predict_user(rs ,user)  # 数组

        # compute the top N items, removing the items that the user already liked
        # from the result and ensure that we don't get out of bounds error when
        # we ask for more recommendations than that are available
        ratings = rs.X_train
        liked = set(ratings[user].indices)  # pos_rating_set
        count = N + len(liked)  # new length
        if count < scores.shape[0]:  # all length

            # when trying to obtain the top-N indices from the score,
            # using argpartition to retrieve the top-N indices in
            # unsorted order and then sort them will be faster than doing
            # straight up argort on the entire score
            # http://stackoverflow.com/questions/42184499/cannot-understand-numpy-argpartition-output
            ids = np.argpartition(scores, -count)[-count:]  # 获取前count大的值的score index
            best_ids = np.argsort(scores[ids])[::-1]  # index排序
            best = ids[best_ids]  # 排好序的index_score list
        else:
            best = np.argsort(scores)[::-1]  # argsort:将x中的元素从小到大排列，提取其对应的index(索引)，然后输出到best

        top_n = list(islice((rec for rec in best if rec not in liked), N))
        return top_n

    def get_similar_items(self, rs, N=5, item_ids=None):
        """
        return the top N similar items for itemid, where
        cosine distance is used as the distance metric

        Parameters
        ----------
        N : int, default 5
            top-N similar items' N

        item_ids : 1d iterator, e.g. list or numpy array, default None
            the item ids that we wish to find the similar items
            of, the default None will compute the similar items
            for all the items

        Returns
        -------
        similar_items : 2d ndarray, shape [number of query item_ids, N]
            each row is the top-N most similar item id for each
            query item id
        """
        # cosine distance is proportional to normalized euclidean distance,
        # thus we normalize the item vectors and use euclidean metric so
        # we can use the more efficient kd-tree for nearest neighbor search;
        # also the item will always to nearest to itself, so we add 1 to
        # get an additional nearest item and remove itself at the end
        normed_factors = normalize(rs.item_factors)
        knn = NearestNeighbors(n_neighbors=N + 1, metric='euclidean')
        knn.fit(normed_factors)

        # returns a distance, index tuple,
        # we don't actually need the distance
        if item_ids is not None:
            normed_factors = normed_factors[item_ids]

        _, items = knn.kneighbors(normed_factors)
        similar_items = items[:, 1:].astype(np.uint32)
        return similar_items


def create_matrix(data, users_col, items_col, ratings_col, threshold=None):
    """
    creates the sparse user-item interaction matrix,
    if the data is not in the format where the interaction only
    contains the positive items (indicated by 1), then use the
    threshold parameter to determine which items are considered positive

    Parameters
    ----------
    data : DataFrame
        implicit rating data

    users_col : str
        user column name

    items_col : str
        item column name

    ratings_col : str
        implicit rating column name

    threshold : int, default None
        threshold to determine whether the user-item pair is
        a positive feedback

    Returns
    -------
    ratings : scipy sparse csr_matrix, shape [n_users, n_items]
        user/item ratings matrix

    data : DataFrame
        implict rating data that retains only the positive feedback
        (if specified to do so)
    """
    data=data.copy()
    if threshold is not None:
        data = data[data[ratings_col] >= threshold]
        data[ratings_col] = 1

    for col in (items_col, users_col, ratings_col):
        data[col] = data[col].astype('category')

    ratings = csr_matrix((data[ratings_col],
                          (data[users_col].cat.codes, data[items_col].cat.codes)))
    ratings.eliminate_zeros()
    return ratings, data


def create_train_test(ratings, test_size=0.2, seed=1234):
    """
    split the user-item interactions matrix into train and test set
    by removing some of the interactions from every user and pretend
    that we never seen them

    Parameters
    ----------
    ratings : scipy sparse csr_matrix, shape [n_users, n_items]
        The user-item interactions matrix

    test_size : float between 0.0 and 1.0, default 0.2
        Proportion of the user-item interactions for each user
        in the dataset to move to the test set; e.g. if set to 0.2
        and a user has 10 interactions, then 2 will be moved to the
        test set

    seed : int, default 1234
        Seed for reproducible random splitting the
        data into train/test set

    Returns
    -------
    train : scipy sparse csr_matrix, shape [n_users, n_items]
        Training set

    test : scipy sparse csr_matrix, shape [n_users, n_items]
        Test set
    """
    assert test_size < 1.0 and test_size > 0.0

    # Dictionary Of Keys based sparse matrix is more efficient
    # for constructing sparse matrices incrementally compared with csr_matrix
    train = ratings.copy().todok()
    test = dok_matrix(train.shape)

    # for all the users assign randomly chosen interactions
    # to the test and assign those interactions to zero in the training;
    # when computing the interactions to go into the test set,
    # remember to round up the numbers (e.g. a user has 4 ratings, if the
    # test_size is 0.2, then 0.8 ratings will go to test, thus we need to
    # round up to ensure the test set gets at least 1 rating)
    rstate = np.random.RandomState(seed)
    for u in range(ratings.shape[0]):
        split_index = ratings[u].indices  # 非0元素对应的列索引值所组成数组
        n_splits = ceil(test_size * split_index.shape[0])  # 上入整数 test个数
        test_index = rstate.choice(split_index, size=n_splits, replace=False)  # 随机选取
        test[u, test_index] = ratings[u, test_index]  # test rating 获取

    train, test = train.tocsr(), test.tocsr()  # dok 转为 csr
    return train, test