import math
import json
from pathlib import Path

HISTORY_FILE = Path("password_history.json")

# Common passwords list (same idea as the video)
COMMON_PASSWORDS = [
    "password", "admin", "123456", "qwerty",
    "pass1234", "letmein", "welcome", "abc123"
]


def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text())
        except:
            return []
    return []


def save_to_history(password):
    history = load_history()
    if password not in history:
        history.append(password)
        HISTORY_FILE.write_text(json.dumps(history, indent=2))


def calculate_entropy(password):
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(not c.isalnum() for c in password):
        pool += 32

    if pool == 0:
        return 0
    return len(password) * math.log2(pool)


def score_password(password):
    score = 0
    length = len(password)

    # Length points
    if length >= 8:
        score += 10
    if length >= 12:
        score += 10

    # Complexity points (same idea as the video)
    if any(c.islower() for c in password):
        score += 10
    if any(c.isupper() for c in password):
        score += 10
    if any(c.isdigit() for c in password):
        score += 10
    if any(not c.isalnum() for c in password):
        score += 15

    # Common password check
    if password.lower() in COMMON_PASSWORDS:
        score = 0

    # Optional: Reuse check
    history = load_history()
    if password in history:
        score = min(score, 20)

    return score


def get_verdict(score):
    if score >= 80:
        return "Very Strong"
    elif score >= 60:
        return "Strong"
    elif score >= 40:
        return "Moderate"
    else:
        return "Weak"


def main():
    print("Password Strength Checker")
    print("-" * 30)

    password = input("Enter a password: ")

    length = len(password)
    entropy = calculate_entropy(password)
    score = score_password(password)
    verdict = get_verdict(score)

    print("\n----- Password Analysis -----")
    print(f"Length   : {length}")
    print(f"Entropy  : {round(entropy, 2)} bits")
    print(f"Score    : {score}/100")
    print(f"Verdict  : {verdict}")

    # Optional reuse feature
    choice = input("\nSave this password to history to prevent reuse? (y/N): ").lower()
    if choice == "y":
        save_to_history(password)
        print("Password saved to history.")


if __name__ == "__main__":
    main()
