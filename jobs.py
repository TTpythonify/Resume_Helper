import requests

# Replace these with your Adzuna app credentials


def get_jobs(query, location, results_per_page=10):
    """
    Fetch jobs from Adzuna API based on query and location
    """
    url = f"https://api.adzuna.com/v1/api/jobs/gb/search/1"  # 'gb' = UK, change if needed
    params = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'results_per_page': results_per_page,
        'what': query,
        'where': location,
        'content-type': 'application/json'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
       
        data = response.json()
        jobs = data.get('results', [])
        print(jobs)
    #     for i, job in enumerate(jobs, 1):
    #         print(f"{i}. {job['title']} at {job['company']['display_name']}")
    #         print(f"   Location: {job['location']['display_name']}")
    #         print(f"   Salary: {job.get('salary_min')} - {job.get('salary_max')}")
    #         print(f"   URL: {job['redirect_url']}\n")
    # else:
        print(f"Error fetching jobs: {response.status_code} {response.text}")


get_jobs("python dev", "ireland")
