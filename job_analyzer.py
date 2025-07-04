import pandas as pd
from job_hunter import JobHunter
import matplotlib.pyplot as plt

def analyze_job_market(search_term="developer", location="london"):
    """Complete job market analysis"""
    
    print(f"Analyzing {search_term} jobs in {location}...")
    
    # Fetch fresh data
    hunter = JobHunter()
    jobs = hunter.search_jobs(what=search_term, where=location)
    csv_file = hunter.save_jobs_to_csv(jobs)
    
    # Load data
    df = pd.read_csv(csv_file)
    
    # Generate comprehensive report
    print("\n" + "="*60)
    print(f"JOB MARKET ANALYSIS: {search_term.upper()} IN {location.upper()}")
    print("="*60)
    
    # Basic stats
    print(f"📊 Total positions: {len(df)}")
    print(f"💰 Salary range: £{df['salary_min'].min():,.0f} - £{df['salary_max'].max():,.0f}")
    print(f"📈 Average salary: £{df['salary_min'].mean():,.0f}")
    print(f"📍 Median salary: £{df['salary_min'].median():,.0f}")
    
    # Top companies
    print("\n🏢 TOP HIRING COMPANIES:")
    top_companies = df['company'].value_counts().head(5)
    for company, count in top_companies.items():
        avg_salary = df[df['company'] == company]['salary_min'].mean()
        print(f"   {company}: {count} jobs (avg £{avg_salary:,.0f})")
    
    # Salary brackets
    print("\n💼 SALARY DISTRIBUTION:")
    salary_brackets = [
        (0, 40000, "Entry Level"),
        (40000, 60000, "Mid Level"),
        (60000, 80000, "Senior"),
        (80000, 100000, "Lead/Principal"),
        (100000, float('inf'), "Executive")
    ]
    
    for min_sal, max_sal, level in salary_brackets:
        count = len(df[(df['salary_min'] >= min_sal) & (df['salary_min'] < max_sal)])
        percentage = (count / len(df)) * 100
        print(f"   {level}: {count} jobs ({percentage:.1f}%)")
    
    # Technology trends
    tech_keywords = ['python', 'javascript', 'react', 'aws', 'docker', 'kubernetes', 'ai', 'machine learning']
    print("\n🔧 TECHNOLOGY TRENDS:")
    for tech in tech_keywords:
        count = df['description'].str.contains(tech, case=False, na=False).sum()
        percentage = (count / len(df)) * 100
        if count > 0:
            print(f"   {tech.title()}: {count} jobs ({percentage:.1f}%)")
    
    # Work arrangements
    remote_count = df['description'].str.contains('remote|Remote', case=False, na=False).sum()
    hybrid_count = df['description'].str.contains('hybrid|Hybrid', case=False, na=False).sum()
    
    print("\n🏠 WORK ARRANGEMENTS:")
    print(f"   Remote-friendly: {remote_count} jobs ({(remote_count/len(df)*100):.1f}%)")
    print(f"   Hybrid: {hybrid_count} jobs ({(hybrid_count/len(df)*100):.1f}%)")
    
    # Save detailed analysis
    analysis_file = f"market_analysis_{search_term}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(analysis_file, 'w') as f:
        f.write(f"Job Market Analysis: {search_term} in {location}\n")
        f.write(f"Generated: {pd.Timestamp.now()}\n")
        f.write(f"Total jobs: {len(df)}\n")
        f.write(f"Average salary: £{df['salary_min'].mean():,.0f}\n")
    
    print(f"\n📋 Analysis saved to {analysis_file}")
    return df

if __name__ == "__main__":
    # Run analysis for different job types
    analyze_job_market("python developer", "london")