import pandas as pd
from job_hunter import JobHunter

def find_entry_level_jobs(csv_file=None):
    """Find and analyze entry-level positions"""
    
    # If no CSV provided, fetch fresh data
    if csv_file is None:
        print("Fetching fresh job data...")
        hunter = JobHunter()
        jobs = hunter.search_jobs(what="developer", where="london")
        csv_file = hunter.save_jobs_to_csv(jobs)
    
    # Load and analyze data
    df = pd.read_csv(csv_file)
    
    # Entry-level indicators
    entry_patterns = [
        'graduate', 'junior', 'entry', 'early career', 
        '1-2 years', 'application developer', 'trainee',
        'associate', 'intern'
    ]
    
    # Filter for entry-level jobs
    pattern = '|'.join(entry_patterns)
    entry_mask = (df['title'].str.contains(pattern, case=False, na=False) | 
                  df['description'].str.contains(pattern, case=False, na=False))
    
    entry_jobs = df[entry_mask].sort_values('salary_min', ascending=False)
    
    # Generate report
    print("\n" + "="*50)
    print("ENTRY-LEVEL OPPORTUNITIES REPORT")
    print("="*50)
    print(f"Total jobs analyzed: {len(df)}")
    print(f"Entry-level positions found: {len(entry_jobs)}")
    print(f"Average entry-level salary: £{entry_jobs['salary_min'].mean():,.0f}")
    
    print("\n🎯 TOP ENTRY-LEVEL POSITIONS:")
    for i, (_, job) in enumerate(entry_jobs.head(5).iterrows(), 1):
        print(f"\n{i}. {job['title']}")
        print(f"   💼 {job['company']}")
        print(f"   💰 £{job['salary_min']:,.0f}")
        print(f"   📍 {job['location']}")
        print(f"   🔗 {job['url']}")
    
    # Save results
    entry_filename = f"entry_level_jobs_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
    entry_jobs.to_csv(entry_filename, index=False)
    print(f"\n📊 Saved {len(entry_jobs)} entry-level jobs to {entry_filename}")
    
    return entry_jobs

if __name__ == "__main__":
    find_entry_level_jobs()