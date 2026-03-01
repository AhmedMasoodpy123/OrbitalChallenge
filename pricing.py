import re

ALL_WORDS = re.compile(r"[A-Za-z'-]+")
VOWELS = set("AEIOUaeiou")

def extract_words(text: str) -> list[str]:
    """A 'word' is any continual sequence of letters, plus ; and -."""
    return ALL_WORDS.findall(text)

def count_third_vowels(text: str) -> int:
    """
    Count occurences whre every 3rd character is a vowel.
    """
    count = 0
    for i in range(2, len(text), 3):
        if text(i) in VOWELS:
            count += 1
        return count
    
def ispalindrome(text: str) -> bool:
    # Step 1: Normalize the text
    cleaned = ""
    for c in text:
        if c.isalnum():
            cleaned += c.lower

    # Step 2: Empty strings shouldn't count    
    if cleaned == "":
        return False
    
    # Step 3: Compare characters from both ends moving inward
    left = 0
    right = len(cleaned) - 1

    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1

    return True

    
def calculate_text_credits(text: str) -> float:
    credits = 1.0 #BaseCost
    credits += 0.05*len(text) #Character count

    words = extract_words(text)

    for i in words:
        n = len(i)
        if n <= 3:
            credits += 0.1
        elif n <= 7:
            credits += 0.2
        else:
            credits += 0.3

    credits += 0.3 * count_third_vowels(text)

    if len(text) > 100:
        credits += 5.0

    if words and len(set(words)) == len(words):
        credits -= 2.0

    if ispalindrome(text):
        credits *= 2.0

    return max(1.0, credits)

    

    


