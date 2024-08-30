# 1. get the name of the person
# 2. get the judgement_text of the person
# 3. prompt + name + judgement_text to llm
import requests
from app.Infra.prompt_gcs import get_prompt
from app.Infra.judgement_bq import get_judgement_pdf

def get_risk_report(name, jlr_link):
    prompt_text = get_prompt()
    judgement_pdf = get_judgement_pdf(jlr_link)
    # Prepare the request payload
    payload = {
        'prompt_text': prompt_text,
        'input_text': judgement_pdf[:6000]
    }
    print(len(judgement_pdf))
    #Send the request to the Flask server
    print('Generating...')
    try:
        response = requests.post('http://10.140.1.79:5000/chat', json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json().get('response', 'No result found')
        print(result)
    except requests.exceptions.RequestException as e:
        result = f"Error: {e}"
    return result
    
#print(get_risk_report("Nguyen Van A", "https://congbobanan.toaan.gov.vn/2ta827827t1cvn/chi-tiet-ban-an"))
