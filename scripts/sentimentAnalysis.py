import openai
from dotenv import load_dotenv
import os

# Load your API key from an environment variable or .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def classify_and_elaborate_prompt(prompt):
    """
    Classifies the given prompt into one of four categories and provides an extended response.
    
    Parameters:
    - prompt: A string containing the user's prompt.
    
    Returns:
    - A string with the classification and an extended response.
    """
    try:
        # Initialize OpenAI client
        client = openai.OpenAI()

        # Template for the system message to guide the AI's response
        system_message = "Classify the following prompt into one of these categories: Urgency, Anxiety/concern, Inquiry, Satisfaction/Dissatisfaction. Then, provide an extended response related to the prompt and its classification. Note that this does not mean you are to provide advice but rather reformat the prompt so that in one line you specify the sentiment of the prompt and then in the next line, you rewrite the prompt in an extended manner, but don't offer medical advice, simply expand upon the prompt since this prompt will be fed onto another model."

        # Create a chat completion request
        response = client.chat.completions.create(
            model="gpt-4",  # Use the GPT-4 model
            max_tokens=3000,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ]
        )

        return response.choices[0].message.content  #note that this is the right syntax for the response (should have just looked at the documentation)

    except Exception as e:
        return str(e)

# Example usage
user_prompt = "I'm really worried about my toothache, what should I do?"
result = classify_and_elaborate_prompt(user_prompt)
print(result)

# save the resulting output:
output_dir = "../sentiment-analysis-output"
os.makedirs(output_dir, exist_ok=True)

response_text = str(result)

# Define the filepath for the text file
txt_file_path = os.path.join(output_dir, "Sentiment_And_Extended_Output.txt")

# Save the response in text format
with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
    txt_file.write(response_text)


