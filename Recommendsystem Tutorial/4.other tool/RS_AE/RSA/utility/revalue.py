from tqdm import tqdm
class ImplicitRevalue:
    def recall(rs, model, num_items=[10]):
        recall_list = []
        for num in num_items:
            print("------------ num_items:", num)
            recall_rate = 0
            for user in tqdm(rs.cg.train_df['user'].drop_duplicates().sort_values()[:-1]):
                item_list = list(rs.cg.test_df[rs.cg.test_df['user'] == user]['item'])
                if len(item_list) > 0:
                    recomm_list = list(model.recommend(rs, user, num_items=num).iloc[:, 0])
                    recall_rate += len(list(set(item_list).intersection(set(recomm_list)))) / len(item_list)
            recall_list.append(recall_rate / len(rs.cg.test_df['user'].drop_duplicates()))
        return recall_list

    def precision(rs, model, num_items=[10]):
        precision_list = []
        for num in num_items:
            print("------------ num_items:", num)
            precision_rate = 0
            for user in tqdm(rs.cg.train_df['user'].drop_duplicates().sort_values()[:-1]):
                item_list = list(rs.cg.test_df[rs.cg.test_df['user'] == user]['item'])
                if len(item_list) > 0:
                    recomm_list = list(model.recommend(rs, user, num_items=num).iloc[:, 0])
                    precision_rate += len(list(set(item_list).intersection(set(recomm_list)))) / len(recomm_list)
            precision_list.append(precision_rate / len(rs.cg.test_df['user'].drop_duplicates()))
        return precision_list


class ExplicitRevalue:
    def recall(rs, model, num_items=[10]):
        recall_list = []
        for num in num_items:
            print("------------ num_items:", num)
            recall_rate = 0
            for user, user_items in tqdm(rs.rg.testSet_u.items()):
                item_list = set(user_items.keys())
                if len(item_list) > 0:
                    recomm_list = set(dict(model.recommend(rs, user, num_items=num)).keys())
                    recall_rate += len(item_list.intersection(recomm_list)) / len(item_list)
            recall_list.append(recall_rate / len(rs.rg.testSet_u))
        return recall_list

    def precision(rs, model, num_items=[10]):
        recall_list = []
        for num in num_items:
            print("------------ num_items:", num)
            precision_rate = 0
            for user, user_items in tqdm(rs.rg.testSet_u.items()):
                item_list = set(user_items.keys())
                if len(item_list) > 0:
                    recomm_list = set(dict(model.recommend(rs, user, num_items=num)).keys())
                    precision_rate += len(item_list.intersection(recomm_list)) / len(recomm_list)
            recall_list.append(precision_rate / len(rs.rg.testSet_u))
        return recall_list

