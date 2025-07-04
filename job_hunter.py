import requests
import pandas as pd
import json
from datetime import datetime
import os
import re

class JobHunter:
    def __init__(self):
        self.api_id = "2971dfe6"  # Replace with your actual API ID
        self.api_key = "898f3aca3f5ce0de9f09a29a720fda1f"  # Replace with your actual API key
        self.base_url = "https://api.adzuna.com/v1/api/jobs/gb"
    
    def search_jobs(self, what="", where="", results_per_page=50, page=1):
        """Search for jobs with given criteria"""
        url = f"{self.base_url}/search/{page}"
        
        params = {
            'app_id': self.api_id,
            'app_key': self.api_key,
            'what': what,
            'where': where,
            'results_per_page': results_per_page,
            'sort_by': 'date'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def search_gov_uk_jobs(self, query="", start=0, count=20):
        """
        Search for jobs using the GOV.UK Search API.
        :param query: Search keywords
        :param start: Offset for pagination
        :param count: Number of results to return
        :return: JSON response with job results
        """
        url = "https://www.gov.uk/api/search.json"
        params = {
            "q": query,
            "start": start,
            "count": count
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_top_companies(self, what=""):
        """Get top companies for a job type"""
        url = f"{self.base_url}/top_companies"
        
        params = {
            'app_id': self.api_id,
            'app_key': self.api_key,
            'what': what
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def clean_job_url(self, url):
        """Clean job URL by removing tracking parameters"""
        if not url:
            return url
        
        if 'adzuna.co.uk' in url:
            job_id_match = re.search(r'/ad/(\d+)', url)
            if job_id_match:
                job_id = job_id_match.group(1)
                return f"https://www.adzuna.co.uk/jobs/details/{job_id}"
        
        # For other sites, remove query parameters
        return url.split('?')[0]
    
    def save_jobs_to_csv(self, jobs_data, filename=None):
        """Save job results to CSV for easy analysis"""
        if filename is None:
            filename = f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        jobs = []
        for job in jobs_data.get('results', []):
            # Clean the URL before saving
            clean_url = self.clean_job_url(job.get('redirect_url', ''))
            
            jobs.append({
                'title': job.get('title', ''),
                'company': job.get('company', {}).get('display_name', ''),
                'location': job.get('location', {}).get('display_name', ''),
                'salary_min': job.get('salary_min', ''),
                'salary_max': job.get('salary_max', ''),
                'description': job.get('description', '')[:200] + '...',
                'url': clean_url,  # Use cleaned URL
                'created': job.get('created', '')
            })
        
        # Save to CSV
        df = pd.DataFrame(jobs)
        df.to_csv(filename, index=False)
        
        print(f"Saved {len(jobs)} jobs to {filename}")
        return filename


# Usage example
if __name__ == "__main__":
    hunter = JobHunter()
    
    # Search for Python developer jobs in London
    jobs = hunter.search_jobs(what="python developer", where="london")
    print(f"Found {jobs['count']} jobs")
    
    # Save to CSV for analysis
    hunter.save_jobs_to_csv(jobs)

    # Search for python jobs on gov
    gov_jobs = hunter.search_gov_uk_jobs(query="python")
    print(f"Found {gov_jobs['total'] if 'total' in gov_jobs else len(gov_jobs.get('results', []))} GOV.UK jobs")

    # # Search for Python jobs on GitHub Jobs
    # github_jobs = hunter.search_github_jobs(description="python", location="london")
    # print(f"Found {len(github_jobs)} GitHub jobs")
    # # You can add a method to save GitHub jobs to CSV if needed
    
    # Get top companies
    companies = hunter.get_top_companies(what="developer")
    print("Top companies:", companies['leaderboard'][:3])