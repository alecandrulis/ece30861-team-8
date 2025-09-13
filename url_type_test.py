from url_process import identify_urltype

url = ""

def url_test(url: str):
    evaluate_url = identify_urltype(url, APIKEY)

    if evaluate_url:
        print(f"\nURL: {url}\nPredicted type: {evaluate_url}")
    else:
        print("Exit FAILURE")