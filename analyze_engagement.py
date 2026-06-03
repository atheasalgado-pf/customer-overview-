import json

def get_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)['values']

def extract_pageviews(data):
    # Header is at row 4 (0-indexed)
    # Organization Name is col 0, Pageview Count is col 5
    pageviews = {}
    for row in data[6:]: # Data starts after headers
        if len(row) > 5:
            name = row[0]
            try:
                views = int(row[5].replace(',', '').strip())
                pageviews[name] = views
            except:
                pass
    return pageviews

apr_data = get_data('apr_usage.json')
mar_data = get_data('mar_usage.json')

apr_views = extract_pageviews(apr_data)
mar_views = extract_pageviews(mar_data)

customers = ["Amplitude", "Appgate", "Cornerstone", "Cotiviti", "Crowdstrike", "Exabeam", "Kinaxis", "KPMG", "Micron", "Modern Health", "Nvidia", "Palo Alto Networks", "Planet", "PWC", "Sysdig", "Thales", "TransUnion"]

for c in customers:
    # Match loosely
    apr_v = next((v for k, v in apr_views.items() if c.lower() in k.lower()), None)
    mar_v = next((v for k, v in mar_views.items() if c.lower() in k.lower()), None)
    print(f"{c}: Mar={mar_v}, Apr={apr_v}")

