import json
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from datasets import Dataset
from sklearn.metrics import precision_score, recall_score, f1_score

# Load the trained model and tokenizer
def load_model_and_tokenizer(model_path):
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    return model, tokenizer

# Load the test data (in the same format as the training data)
def load_test_data(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
    
    input_lines = []
    label_lines = []
    for entry in data:
        # Append the 'Content' field to input_lines
        input_lines.append(entry['Content'])
        
        # Append the 'Aspects' field (concatenated terms) to label_lines
        aspects = [term for aspect in entry['Aspects'] for term in aspect['AspectTerms']]
        label_lines.append(' '.join(aspects))  # Join the aspect terms into a single string
    
    return input_lines, label_lines

# Preprocess the input text for the model
def preprocess_input(input_texts, tokenizer, max_length=128):
    return tokenizer(input_texts, return_tensors="pt", truncation=True, padding=True, max_length=max_length)

# Run inference using the trained model
def generate_predictions(input_texts, model, tokenizer, max_length=128, num_beams=4):
    model.eval()  # Set model to evaluation mode
    inputs = preprocess_input(input_texts, tokenizer, max_length)

    # Perform inference with beam search for better predictions
    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_length=max_length,
            num_beams=num_beams,
            early_stopping=True
        )

    # Decode the output tokens to text
    decoded_outputs = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    return decoded_outputs

# Evaluate the predictions with ground truth labels (if available)
def evaluate_predictions(predicted_aspects, ground_truth_aspects):
    all_possible_aspects = set()  # Set to store all possible aspects in the test data

    # Collect all unique aspects
    for aspects in ground_truth_aspects:
        all_possible_aspects.update(aspects.split())

    all_possible_aspects = list(all_possible_aspects)  # Convert set to list

    # Vectorize the aspect terms (binary vectors)
    def binary_vectorize(aspect_list, all_possible_aspects):
        return [1 if aspect in aspect_list else 0 for aspect in all_possible_aspects]

    y_true = [binary_vectorize(gt.split(), all_possible_aspects) for gt in ground_truth_aspects]
    y_pred = [binary_vectorize(pred.split(), all_possible_aspects) for pred in predicted_aspects]

    precision = precision_score(y_true, y_pred, average='macro')
    recall = recall_score(y_true, y_pred, average='macro')
    f1 = f1_score(y_true, y_pred, average='macro')

    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")

# Test module function that loads the model, test data, performs inference, and evaluates
def test_model(model_path, test_json_file):
    # Step 1: Load the trained model and tokenizer
    model, tokenizer = load_model_and_tokenizer(model_path)

    # Step 2: Load the test data (in the same JSON format as training data)
    test_inputs, ground_truth_aspects = load_test_data(test_json_file)

    # Step 3: Generate predictions for the test data
    predicted_aspects = generate_predictions(test_inputs, model, tokenizer)

    # Step 4: Print the predictions
    for i, input_text in enumerate(test_inputs):
        print(f"Input: {input_text}")
        print(f"Predicted Aspects: {predicted_aspects[i]}")
        print(f"Ground Truth Aspects: {ground_truth_aspects[i]}")
        print()

    # Step 5: Evaluate the predictions
    evaluate_predictions(predicted_aspects, ground_truth_aspects)

# Example usage of the test module
if __name__ == "__main__":
    model_path = "sample_data/Sep23"  # Path to the trained model directory
    test_json_file = "label_subset.json"  # Path to the test JSON file

    test_model(model_path, test_json_file)