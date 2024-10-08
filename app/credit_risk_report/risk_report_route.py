import re
from flask import request, jsonify
from app.credit_risk_report.risk_report import get_risk_report

def report_generate():
    if request.method == 'POST':
        data = request.get_json()
        # check identical result
        if data['identical_results'] != []:
            name = data['identical_results'][0]['name']
            jlr_link_html= data['identical_results'][0]['jlr_link']
            url_match = re.search(r'href="([^"]+)"', jlr_link_html)
            
            if url_match:
                jlr_link_html = url_match.group(1)
                
            print(name, jlr_link_html)
            risk_report = get_risk_report(name, jlr_link_html)
            
            print(risk_report)
            return jsonify(risk_report=risk_report)
            
        else:
            name = data['similar_results'][0]['name']
            jlr_link_html= data['similar_results'][0]['jlr_link']
            url_match = re.search(r'href="([^"]+)"', jlr_link_html)
            if url_match:
                jlr_link_html = url_match.group(1)
                
            print(name, jlr_link_html)
            risk_report = get_risk_report(name, jlr_link_html)
            print(risk_report)
            return jsonify(risk_report=risk_report)
            raise "No identical result found"

