from flask import request, jsonify
from app.credit_risk_report.comparison_chris import vector_search

def compare_route():
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('personName')
        gender = data.get('personGender')
        address = data.get('personAddress')
        birthdate = data.get('personBirthdate')
        formatted_birthdate = birthdate.replace('-', '/')
        result = vector_search(name, gender, address, formatted_birthdate)

        identical_result, similar_result = result['identical'], result['top_5_similar']
        # Return dataset shape and head as JSON
        return jsonify(identical_result=identical_result, similar_result=similar_result)
