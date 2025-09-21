from openai import OpenAI
import json

def extract_job_keywords(user_sentence):
    """
    Extracts job title, location, and skills from a user-provided sentence using GPT-3.5-turbo.
    
    Args:
        user_sentence (str): Full sentence describing the desired job.
    
    Returns:
        dict: Dictionary containing 'job_title', 'location', and 'skills'.
    """
    prompt = f"""
    Extract the job title, location, and skills from this text and return as valid JSON:
    "{user_sentence}"
    """
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    output_text = response.choices[0].message.content
    
    try:
        keywords = json.loads(output_text)
    except json.JSONDecodeError:
        # Fallback if GPT output is invalid
        keywords = {
            "job_title": user_sentence,
            "location": "",
            "skills": []
        }
    
    return keywords

# # Example usage
# user_sentence = "I want an entry role for software engineering.  i like python, java and backend developement. i live in dublin but i want to work in cork and sligo"
# keywords = extract_job_keywords(user_sentence)
# print(keywords)
