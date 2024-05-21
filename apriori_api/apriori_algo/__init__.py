

def get_recommendations(basket, rules, num_recommendations=5):
    basket_set = set(basket)
    print(basket_set)
    applicable_rules = rules[rules['antecedents'].apply(lambda x: basket_set.issubset(x))]
    applicable_rules = applicable_rules.sort_values(by='confidence', ascending=False)
    recommendations = set()
    for _, rule in applicable_rules.iterrows():
        consequents = rule['consequents']
        recommendations.update(consequents)
        if len(recommendations) >= num_recommendations:
            break
    recommendations = recommendations - basket_set

    return list(recommendations)[:num_recommendations]
