import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import json

# Configuration for the Generative AI
genai.configure(api_key="AIzaSyA6t6yawckjVx4zDWorU8rTpWYYgACm6pk")
chatbot_model = genai.GenerativeModel("gemini-2.0-flash")
bert_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# Chatbot Evaluation Function
def chatbot_evaluate(question, student_answer, max_marks):
    prompt = (
        f"You are an AI evaluator. Given a question, a student's response, and total marks, "
        f"assign a score as follows: "
        f"1. Full marks for correct response. "
        f"2. Partial marks for partially correct answers. "
        f"3. Zero marks for incorrect or irrelevant answers. "
        f"Format your output as a number: <marks> (e.g., 5). "
        f"For unrelated prompts, return 0. "
        f"Strictly respond with a number only.\n\n"
        f"Question: {question}\n"
        f"Student Response: {student_answer}\n"
        f"Total Marks: {max_marks}"
    )
    print("Sending request to Chatbot API...", flush=True)
    response = chatbot_model.generate_content(prompt)
    try:
        chatbot_score = int(response.text.strip())
    except ValueError:
        chatbot_score = 0
    print(f"Chatbot Response: {response.text.strip()}", flush=True)
    print(f"Final Chatbot Score: {chatbot_score}", flush=True)
    return max(0, min(chatbot_score, max_marks))

# Function to calculate BERT score
def calculate_bert_score(model_answer, student_answer, max_marks):
    embeddings = bert_model.encode([model_answer, student_answer])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    
    # Apply stricter threshold and non-linear cubic scaling
    min_similarity = 0.6
    if similarity < min_similarity:
        bert_score = 0
    else:
        normalized_similarity = (similarity - min_similarity) / (1 - min_similarity)
        bert_score = round((normalized_similarity ** 3) * max_marks)
        bert_score = max(0, min(bert_score, max_marks))
    
    print(f"BERT Score Calculated: {bert_score}", flush=True)
    return bert_score

# Function to simulate test submission
def submit_test(question, student_answer, model_answer, max_marks):
    print(f"Processing Question: {question}")
    print(f"Student Answer: {student_answer}")
    print(f"Model Answer: {model_answer}")
    print(f"Max Marks: {max_marks}")
    
    # Calculate BERT score
    bert_score = calculate_bert_score(model_answer, student_answer, max_marks)
    
    # Get chatbot evaluation score
    chatbot_score = chatbot_evaluate(question, student_answer, max_marks)
    
    # Average the two scores
    final_score = round((bert_score + chatbot_score) / 2)
    print(f"Final Computed Score: {final_score}", flush=True)
    return final_score

# Sample data to test the code
question = "What is the capital of France?"
student_answer = "Paris is the capital of Berlin."
model_answer = "Paris is the capital city of France."
max_marks = 10

# Test the code
submit_test(question, student_answer, model_answer, max_marks)
