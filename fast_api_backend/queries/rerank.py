from sentence_transformers import CrossEncoder

model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', max_length=512)

def get_reranked(results, near_text):
    data = []
    for res in results:
        description = ''
        for des in res['work_descriptions']:
            description += des
        for cmp in res['companies']:
            description += cmp
        data.append((near_text, description))
    
    scores = model.predict(data)
    print(scores)
    
    # Pair each result with its corresponding score
    results_with_scores = list(zip(results, scores))
    
    # Sort the results based on the scores (assuming higher scores are better)
    sorted_results_with_scores = sorted(results_with_scores, key=lambda x: x[1], reverse=True)
    
    # Extract the sorted results
    sorted_results = [result for result, score in sorted_results_with_scores]
    
    return sorted_results
