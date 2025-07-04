import pandas as pd
import re

def clean_adzuna_url(url):
    """Clean Adzuna URLs by removing query parameters and simplifying structure"""
    if pd.isna(url) or not url:
        return url
    
    # For Adzuna URLs, extract job ID and create clean URL
    if 'adzuna.co.uk' in url:
        try:
            # Extract job ID from various URL patterns
            job_id_match = re.search(r'/ad/(\d+)', url)
            if job_id_match:
                job_id = job_id_match.group(1)
                return f"https://www.adzuna.co.uk/jobs/details/{job_id}"
            
            # If no job ID found, just remove query parameters
            return url.split('?')[0]
        except:
            return url.split('?')[0]
    
    # For other URLs, remove query parameters
    return url.split('?')[0]

def clean_csv_urls(filename):
    """Clean URLs in the CSV file"""
    # Read the CSV
    df = pd.read_csv(filename)
    
    print(f"Cleaning {len(df)} job URLs...")
    
    # Clean the URLs
    df['url'] = df['url'].apply(clean_adzuna_url)
    
    # Create new filename
    clean_filename = filename.replace('.csv', '_cleaned.csv')
    
    # Save cleaned CSV
    df.to_csv(clean_filename, index=False)
    
    print(f"✅ Cleaned URLs saved to: {clean_filename}")
    
    # Show examples
    print("\n📝 Sample cleaned URLs:")
    for i in range(min(50, len(df))):
        print(f"   {df.iloc[i]['title'][:50]}...")
        print(f"   🔗 {df.iloc[i]['url']}")
        print()
    
    return clean_filename

if __name__ == "__main__":
    # Clean your file
    filename = "jobs_20250703_155620.csv"
    clean_csv_urls(filename)



# adding this endpoint as well, for remote jobs in uk:
# https://jobicy.com/categories/dev