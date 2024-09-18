import pandas as pd
import openai
import os

# Enter your API key here
openai.api_key = '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'

model = "gpt-3.5-turbo"
csv_file_path = "test.csv"  # Update this to the path of your CSV file

# Load your CSV data into a pandas DataFrame
df = pd.read_csv(csv_file_path)

# Check if the 'completion' column exists, if not, add it
if 'Completion' not in df.columns:
    df['Completion'] = pd.Series([None] * len(df))

def generate_chat_completion(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": 'You are an aspect based sentiment analysis expert in Vietnamese. Find me all aspects and their polarity for the following text. Please response in json format.'},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating chat completion for prompt: {prompt}\nError: {e}")
        return ""

# Process each prompt individually
for index, row in df.iterrows():
    df.at[index, 'Completion'] = generate_chat_completion('Text: ' + row['Content'] + '. Aspect')

# Save the updated dataframe back to a TSV file
df.to_csv('inference_gpt_turbo.csv', index=False)
