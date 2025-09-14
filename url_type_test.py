from url_process import identify_urltype
from API_KEY import APIKEY

def url_test(url: str):
    evaluate_url = identify_urltype(url, APIKEY)

    if evaluate_url:
        print(f"\nURL: {url}\nPredicted type: {evaluate_url}")
    else:
        print("Exit FAILURE")


def main():
    url = "https://huggingface.co/datasets/facebook/recycling_the_web"
    url_test(url)


if __name__ == "__main__":
    main()