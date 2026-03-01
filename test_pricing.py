from pricing import extract_words, count_third_vowels, ispalindrome, calculate_text_credits


def test_extract_words_apostrophes_and_hyphens():
    # Validates the spec word definition: letters plus ' and -
    text = "don't do long-term leases"
    assert extract_words(text) == ["don't", "do", "long-term", "leases"]


def test_count_third_vowels_positions():
    # 3rd char is 'E' (vowel), 6th char is 'f' (not vowel)
    text = "abEdef"
    assert count_third_vowels(text) == 1


def test_unique_word_bonus_case_sensitive():
    # Case-sensitive uniqueness: "Hi" and "hi" are different => unique bonus should apply
    unique_case = "Hi hi"
    not_unique = "hi hi"
    assert calculate_text_credits(unique_case) < calculate_text_credits(not_unique)


def test_palindrome_doubles_and_minimum_floor_holds():
    # A single letter becomes a palindrome after normalization.
    # This also indirectly tests that credits never drop below 1.
    assert ispalindrome("A") is True
    assert calculate_text_credits("A") >= 1.0