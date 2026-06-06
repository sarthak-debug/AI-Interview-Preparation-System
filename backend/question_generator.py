QUESTION_BANK = {
    "python": [
        "What is a decorator in Python?",
        "Difference between list and tuple?",
        "What is a lambda function?"
    ],
    "react": [
        "What is Virtual DOM?",
        "Difference between State and Props?",
        "What are React Hooks?"
    ],
    "sql": [
        "Difference between DELETE and TRUNCATE?",
        "What is a JOIN?",
        "What is normalization?"
    ],
    "git": [
        "What is Git?",
        "Difference between merge and rebase?",
        "What is a pull request?"
    ],
    "javascript": [
        "What is closure?",
        "Difference between let, var and const?",
        "What is event bubbling?"
    ]
}

def generate_questions(skills):
    questions = []

    for skill in skills:
        if skill in QUESTION_BANK:
            questions.extend(QUESTION_BANK[skill])

    return questions