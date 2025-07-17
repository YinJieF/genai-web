from vertexai.preview.language_models import TextEmbeddingModel, TextEmbeddingInput
from scipy.spatial.distance import cosine
from google.cloud import bigquery

def embed_text(input_texts, weight, model_name="text-multilingual-embedding-002"):
    """
    將輸入的文字列表轉換為向量。

    Args:
        input_texts (list of str): 要轉換的文字列表。
        model_name (str): 使用的模型名稱。
        task (str): 嵌入任務類型。

    Returns:
        list of list: 每個文字對應的嵌入向量。
    """
    model = TextEmbeddingModel.from_pretrained(model_name)
    #inputs = [TextEmbeddingInput(text, task) for text in input_texts]
    embeddings = model.get_embeddings([input_texts])
    # 返回嵌入向量列表
    return [x * weight for x in list(embeddings[0].values)]

def vector_search(input_name, input_gender, input_address, input_birthday,top_k = 5, distance_type = 'COSINE',TRANS_TYPE_OF_CASE = '刑事'):
    
    client = bigquery.Client()
    project_id = 'PROJECT_ID'
    dataset_id = 'DATASET_ID'
    table_id = 'TABLE_ID'
    
    name_vector = embed_text(input_name, weight = 1000)
    gender_vector = embed_text(input_gender, weight = 100)
    address_vector = embed_text(input_address, weight =300)
    birthday_vector = embed_text(input_birthday, weight =500)
    addition_vector = [sum(x) for x in zip(*[name_vector, gender_vector, address_vector, birthday_vector])]
    # Construct the SQL query
    query = f"""
    SELECT *
    FROM VECTOR_SEARCH(
      (SELECT * FROM `{project_id}.{dataset_id}.{table_id}` WHERE TRANS_TYPE_OF_CASE = '{TRANS_TYPE_OF_CASE}'), 'embeddings',
      (SELECT {addition_vector} AS embed), top_k => {top_k}, distance_type => '{distance_type}')
    """
    # Run the query
    query_job = client.query(query)
    # Fetch results
    results = query_job.result() # results = {'query':{'embed':[vector]}, 'base':{table columns}, 'distance': distance}
    # Convert results to a list of dictionaries
    result_dict = dict()
    result_dict['identical'] = []
    result_dict['top_5_similar'] = []
    for result in results: 
        #print(result['distance'])
        result_dict['top_5_similar'].append({'jlr_link': result['base']['JLR_LINK'], 
                                       'crime': result['base']['TRANS_TYPE_OF_CASE'],
                                       'name': result['base']['name_llm_llama'], 
                                       'full_address': result['base']['address_llm_llama'],
                                       'gender': result['base']['gender_llm_llama'], 
                                       'birthdate': result['base']['birthday_llm_llama'],
                                       'total_similarity': 100 - (result['distance'] * 100)#(((1 - result['distance']) * 100 - 85) / (100 -85)) * 100
                                      })
    # Sort 'top_5_similar' by 'total_similarity' in descending order
    result_dict['top_5_similar'].sort(key=lambda x: x['total_similarity'], reverse=True)

    # Append the person with the highest similarity to 'identical'
    if result_dict['top_5_similar']:
        highest_similarity_person = result_dict['top_5_similar'][0]  # Get the person with the highest similarity
        result_dict['identical'].append(highest_similarity_person)
    
    return result_dict
