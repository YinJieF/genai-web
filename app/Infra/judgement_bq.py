from google.cloud import bigquery

# Get the full judgement pdf of a case by jlr_link
def query_for_pdf(jlr_link):
    client = bigquery.Client()
    
    query = f"""
        SELECT PDF_CONTENT
        FROM `PROJECT_ID.DATASET_ID.TABLE_ID`
        WHERE CASE_LINK = '{jlr_link}'
    """
    try:
        query_job = client.query(query)
        result = query_job.result()
        for row in result:
            result = row.PDF_CONTENT
        return result
    except Exception as e:
        print(f"Query failed: {e}")
        return ""

def get_judgement_pdf(jlr_link):
    if isinstance(jlr_link, str):
        return query_for_pdf(jlr_link)
    return [query_for_pdf(link) for link in jlr_link]

# jlr_link = 'https://congbobanan.toaan.gov.vn/2ta827827t1cvn/chi-tiet-ban-an'
# jlr_link_list = ['https://congbobanan.toaan.gov.vn/2ta827827t1cvn/chi-tiet-ban-an',
#                  'https://congbobanan.toaan.gov.vn/2ta889668t1cvn/chi-tiet-ban-an',
#                  'https://congbobanan.toaan.gov.vn/2ta153804t1cvn/chi-tiet-ban-an']

# print(get_judgement_pdf(jlr_link))
# print(get_judgement_pdf(jlr_link_list))
