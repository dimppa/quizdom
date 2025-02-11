import os
import argparse
import random
from datetime import datetime

def load_quiz(quiz_path):
    """Load and parse the quiz file into a structured format."""
    with open(quiz_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    questions = []
    current_question = {}
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('Q'):
            if current_question:
                questions.append(current_question)
            current_question = {
                'question': line.split(':', 1)[1].strip(),
                'options': {},
                'correct_answer': None,
                'original_correct_text': None
            }
        elif line.startswith(('A)', 'B)', 'C)', 'D)')):
            option_letter = line[0]
            option_text = line[2:].strip()
            current_question['options'][option_letter] = option_text
        elif line.startswith('Answer:'):
            correct_letter = line.split(':')[1].strip()[0]
            current_question['original_correct_text'] = current_question['options'][correct_letter]
            
            # Randomize the options
            options_text = list(current_question['options'].values())
            random.shuffle(options_text)
            
            # Reassign the shuffled options to letters
            current_question['options'] = {}
            for i, letter in enumerate(['A', 'B', 'C', 'D']):
                current_question['options'][letter] = options_text[i]
                if options_text[i] == current_question['original_correct_text']:
                    current_question['correct_answer'] = letter

    if current_question:
        questions.append(current_question)
        
    return questions

def take_quiz(questions):
    """Present the quiz to the user and collect answers."""
    print("\nWelcome to the Quiz!\n")
    user_answers = {}
    total_questions = len(questions)

    for i, q in enumerate(questions, 1):
        print(f"\nQuestion {i} of {total_questions}:")
        print(q['question'])
        
        for letter, text in q['options'].items():
            print(f"{letter}) {text}")
            
        while True:
            answer = input("\nYour answer (A/B/C/D): ").strip().upper()
            if answer in ['A', 'B', 'C', 'D']:
                user_answers[i] = answer
                break
            print("Invalid input. Please enter A, B, C, or D.")

    return user_answers

def grade_quiz(questions, user_answers):
    """Grade the quiz and return results."""
    correct = 0
    results = []
    
    for i, q in enumerate(questions, 1):
        user_answer = user_answers.get(i)
        correct_answer = q['correct_answer']
        is_correct = user_answer == correct_answer
        
        if is_correct:
            correct += 1
            
        results.append({
            'question_num': i,
            'question': q['question'],
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct
        })
    
    return correct, len(questions), results

def display_results(correct, total, results):
    """Display the quiz results."""
    print("\n=== Quiz Results ===")
    print(f"Score: {correct}/{total} ({(correct/total)*100:.1f}%)\n")
    
    print("Question Summary:")
    for r in results:
        status = "✓" if r['is_correct'] else "✗"
        print(f"\nQ{r['question_num']}: {status}")
        print(f"Your answer: {r['user_answer']}")
        if not r['is_correct']:
            print(f"Correct answer: {r['correct_answer']}")

def get_latest_quiz(quiz_dir):
    """Get the most recently created quiz file."""
    quiz_files = [f for f in os.listdir(quiz_dir) if f.endswith('_quiz.txt')]
    if not quiz_files:
        return None
    
    quiz_files_with_time = [(f, os.path.getctime(os.path.join(quiz_dir, f))) 
                           for f in quiz_files]
    quiz_files_with_time.sort(key=lambda x: x[1], reverse=True)
    
    return quiz_files_with_time[0][0]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--latest', action='store_true', 
                       help='Automatically select the most recent quiz')
    parser.add_argument('--random', action='store_true',
                       help='Randomly select a quiz')
    args = parser.parse_args()

    quiz_dir = "quizzes"
    
    if args.latest:
        # Automatically select the latest quiz
        selected_quiz = get_latest_quiz(quiz_dir)
        if not selected_quiz:
            print("No quiz files found!")
            return
        print(f"Loading latest quiz: {selected_quiz}")
    else:
        # List all quiz files
        quiz_files = [f for f in os.listdir(quiz_dir) if f.endswith('_quiz.txt')]
        
        if not quiz_files:
            print("No quiz files found in the quizzes directory!")
            return

        if args.random:
            # Randomly select a quiz
            selected_quiz = random.choice(quiz_files)
            print(f"Randomly selected: {selected_quiz}")
        else:
            # Display available quizzes
            print("Available quizzes:")
            for i, file in enumerate(quiz_files, 1):
                creation_time = datetime.fromtimestamp(
                    os.path.getctime(os.path.join(quiz_dir, file))
                ).strftime('%Y-%m-%d %H:%M:%S')
                print(f"{i}. {file} (created: {creation_time})")
                
            print("\nOptions:")
            print("Enter a number to select a specific quiz")
            print("Or type 'r' for a random quiz")
            
            # Let user select a quiz
            while True:
                choice = input("\nYour choice: ").strip()
                if choice.lower() == 'r':
                    selected_quiz = random.choice(quiz_files)
                    print(f"Randomly selected: {selected_quiz}")
                    break
                try:
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(quiz_files):
                        selected_quiz = quiz_files[choice_num - 1]
                        break
                    print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a number or 'r' for random.")
    
    quiz_path = os.path.join(quiz_dir, selected_quiz)
    questions = load_quiz(quiz_path)
    user_answers = take_quiz(questions)
    correct, total, results = grade_quiz(questions, user_answers)
    display_results(correct, total, results)

if __name__ == "__main__":
    main()
