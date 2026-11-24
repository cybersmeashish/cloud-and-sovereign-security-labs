from site_service import serve_cases

def run(root,output):
    rows=serve_cases()
    return {"scope":"actual loopback HTTP exchanges under synthetic policy/time/actor inputs; central unavailability is a fixture condition, not a provider outage","http_cases":len(rows),"rows":rows,"real_identity_integration":False,"provider_deployment":False}
