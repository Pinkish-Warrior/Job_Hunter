from job_hunter import JobHunter
import pandas as pd

def search_tech_jobs_comprehensive():
    """Comprehensive tech job search for London"""
    
    hunter = JobHunter()
    
    # Define tech job categories
    tech_searches = [
        "software developer london",
        "software engineer london", 
        "web developer london",
        "data analyst london",
        "business analyst london",
        "python developer london",
        "javascript developer london",
        "frontend developer london",
        "backend developer london",
        "full stack developer london",
        "devops engineer london",
        "cybersecurity analyst london",
        "IT support london",
        "technical analyst london",
        "digital marketing london",
        "UX designer london",
        "product manager london"
    ]
    
    all_jobs = []
    
    for search_term in tech_searches:
        try:
            print(f"🔍 Searching: {search_term}")
            jobs = hunter.search_jobs(what=search_term, where="", results_per_page=50)
            
            for job in jobs.get('results', []):
                job['search_category'] = search_term.replace(' london', '')
                all_jobs.append(job)
                
        except Exception as e:
            print(f"❌ Error with {search_term}: {e}")
            continue
    
    # Remove duplicates
    unique_jobs = []
    seen_urls = set()
    
    for job in all_jobs:
        url = job.get('redirect_url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_jobs.append(job)
    
    # Create CSV with additional tech info
    tech_data = []
    for job in unique_jobs:
        tech_data.append({
            'title': job.get('title', ''),
            'company': job.get('company', {}).get('display_name', ''),
            'location': job.get('location', {}).get('display_name', ''),
            'salary_min': job.get('salary_min', ''),
            'salary_max': job.get('salary_max', ''),
            'search_category': job.get('search_category', ''),
            'description': job.get('description', '')[:300] + '...',
            'url': job.get('redirect_url', ''),
            'created': job.get('created', '')
        })
    
    # Save to CSV
    df = pd.DataFrame(tech_data)
    filename = f"tech_jobs_london_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    
    print(f"\n✅ Found {len(unique_jobs)} unique tech jobs")
    print(f"📊 Saved to {filename}")
    
    # Quick analysis
    print(f"\n📈 TECH JOB BREAKDOWN:")
    category_counts = df['search_category'].value_counts().head(10)
    for category, count in category_counts.items():
        print(f"   {category}: {count} jobs")
    
    return filename

if __name__ == "__main__":
    search_tech_jobs_comprehensive()