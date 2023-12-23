import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta

customer_interactions = pd.read_csv("data/customer_interactions.csv")
product_details = pd.read_csv("data/product_details.csv")
purchase_history = pd.read_csv("data/purchase_history.csv")
product_details_processed = pd.read_csv("data/product_details_processed.csv")
product_purchase_history = pd.read_csv("data/product_purchase_history.csv")


def get_recommendation(cust_id, n, n_baseline=100):
    user_profiles = product_purchase_history[product_purchase_history.customer_id == cust_id]
    user_profiles = user_profiles.head(n_baseline)

    if len(user_profiles) == 0:
        return f"Customer ID {cust_id} Not Found"

    fields = ["price", "ratings", "category_Beauty", "category_Clothing", "category_Electronics", "category_Home Decor"]
    n_per_sample = math.ceil(n/len(user_profiles))

    if n_per_sample < 2:
        n_per_sample = 2

    df_recoms = pd.DataFrame([])
    for index, user_profile in user_profiles.iterrows():
        df_recom = pd.DataFrame([])

        user_profile_data = [user_profile[fields].values]
        product_profile_data = product_details_processed[fields].values
        similarity_scores = cosine_similarity(user_profile_data, product_profile_data)
        
        closest_ids = similarity_scores.argsort()[::-1]
        closest_ids = closest_ids[0][-n_per_sample-1:-1]
        
        product_recom = product_details.iloc[
            closest_ids
        ]
        similarity_scores_recom = similarity_scores[0][closest_ids]
        delta = relativedelta(datetime.now(), pd.to_datetime(user_profile.purchase_date))
        total_days = delta.days + delta.years * 365 + delta.months * 30

        df_recom["history_product_id"] = \
            [user_profile.product_id] * len(product_recom)
        df_recom["recency"] = \
            [delta] * len(product_recom)
        df_recom["recommend_product_id"] = product_recom.product_id.values
        df_recom["similarity_scores_recom"] = similarity_scores_recom
        df_recom["overall_score"] = df_recom["similarity_scores_recom"] / math.log(total_days)
        
        df_recoms = pd.concat([df_recoms, df_recom])

    df_recoms = df_recoms.sort_values(by='overall_score', ascending=False)
    df_recoms = df_recoms.reset_index()
    return df_recoms.head(n)

