import pandas as pd

# Cognitive Computing Assignment
# Roll Number: 1024170274
# Questions 1-6 in one Python file

ROLL_NUMBER = "1024170274"

# ----------------------------- Q1 ---------------------------------
# Four fixed FAQ entries given in the assignment.
fixed_entries = [
    {
        "question": "what is the annual fee",
        "answer": "The annual fee is Rs 500.",
        "keywords": ["fee", "cost", "price", "charge"],
        "category": "billing",
    },
    {
        "question": "how to reset password",
        "answer": "Go to Settings > Reset Password.",
        "keywords": ["password", "reset", "login"],
        "category": "account",
    },
    {
        "question": "what are your working hours",
        "answer": "We are open 9 AM to 5 PM.",
        "keywords": ["hours", "timing", "open time"],
        "category": "general",
    },
    {
        "question": "how can i pay the fee",
        "answer": "You can pay via UPI, card, or net banking.",
        "keywords": ["pay", "payment", "upi", "fee"],
        "category": "billing",
    },
]


def make_personalized_entry(digit, position):
    """Create one FAQ entry using the category rule from the assignment."""
    categories = ["billing", "account", "general"]
    category = categories[digit % 3]

    # Create a realistic question and suitable keywords for each category.
    examples = {
        "billing": (
            f"how can i check my bill for digit {digit}",
            "You can check your bill in the Billing section.",
            ["bill", "billing", "payment", "amount"],
        ),
        "account": (
            f"how can i update my account details for digit {digit}",
            "Open Account Settings to update your personal details.",
            ["account", "profile", "details", "update"],
        ),
        "general": (
            f"where can i get help for digit {digit}",
            "You can contact support through the Help section.",
            ["help", "support", "assistance", "contact"],
        ),
    }

    question, answer, keywords = examples[category]
    return {
        "question": question,
        "answer": answer,
        "keywords": keywords,
        "category": category,
    }


last_two_digits = ROLL_NUMBER[-2:]
personalized_entries = [
    make_personalized_entry(int(digit), position)
    for position, digit in enumerate(last_two_digits, start=1)
]

# Exactly six entries: four fixed + two personalized.
faq_entries = fixed_entries + personalized_entries
df = pd.DataFrame(faq_entries)

print("\\n" + "=" * 65)
print("Q1: PERSONALIZED KNOWLEDGE BASE")
print("Roll number:", ROLL_NUMBER)
print("Last two digits:", last_two_digits)
print(df.to_string(index=False))


# ----------------------------- Q2 ---------------------------------
def score_hypothesis(query, dataframe=df):
    """
    Return every FAQ entry that matches the query, ranked by confidence.
    Confidence = number of matched keywords / total keywords for that entry.
    """
    query_words = set(query.lower().split())
    results = []

    for index, entry in dataframe.iterrows():
        keywords = [str(word).lower() for word in entry["keywords"]]
        matched = [word for word in keywords if word in query_words]

        if matched:
            confidence = len(matched) / len(keywords) if keywords else 0
            results.append({
                "index": index,
                "question": entry["question"],
                "category": entry["category"],
                "matched_keywords": matched,
                "score": confidence,
            })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results


print("\\n" + "=" * 65)
print("Q2: HYPOTHESIS SCORING")
q2_query = input("Enter a query for Q2 (e.g. fee or reset password): ").strip()
q2_results = score_hypothesis(q2_query)

if q2_results:
    for result in q2_results:
        print(
            f"Question: {result['question']} | "
            f"Category: {result['category']} | "
            f"Matched: {result['matched_keywords']} | "
            f"Confidence: {result['score']:.2f}"
        )
else:
    print("No matching FAQ entry found.")


# ----------------------------- Q3 ---------------------------------
def same_category(category_name, dataframe=df):
    """Return all FAQ questions belonging to the requested category."""
    category_name = category_name.strip().lower()
    return dataframe[
        dataframe["category"].str.lower() == category_name
    ]["question"].tolist()


print("\\n" + "=" * 65)
print("Q3: SAME CATEGORY")
# Use the category of the first personalized entry, as required.
selected_category = personalized_entries[0]["category"]
print("Selected personalized-entry category:", selected_category)
print("Questions in this category:")
for question in same_category(selected_category):
    print("-", question)


# ----------------------------- Q4 ---------------------------------
print("\\n" + "=" * 65)
print("Q4: ADD A NEW KEYWORD")
print("Choose an FAQ entry by its displayed index:")
for index, entry in df.iterrows():
    print(f"{index}: {entry['question']}")

try:
    selected_index_text = input("Enter entry index (0-5): ").strip()
    selected_index = int(selected_index_text)

    if selected_index not in df.index:
        print("Invalid index. No keyword was added.")
    else:
        new_keyword = input("Enter the new keyword to add: ").strip().lower()

        if new_keyword:
            updated_keywords = list(df.at[selected_index, "keywords"])
            if new_keyword not in updated_keywords:
                updated_keywords.append(new_keyword)
                df.at[selected_index, "keywords"] = updated_keywords
                print("Keyword added successfully.")
            else:
                print("That keyword already exists in this entry.")

            # Save the complete updated knowledge base to CSV.
            csv_filename = f"{ROLL_NUMBER}_faq_data.csv"
            csv_df = df.copy()
            csv_df["keywords"] = csv_df["keywords"].apply(
                lambda words: ", ".join(words)
            )
            csv_df.to_csv(csv_filename, index=False)
            print(f"Updated knowledge base saved to: {csv_filename}")
        else:
            print("No keyword entered. Knowledge base was not changed.")
except ValueError:
    print("Invalid input. Please enter a number from 0 to 5.")


# ----------------------------- Q5 ---------------------------------
print("\\n" + "=" * 65)
print("Q5: NUMBER OF FAQ ENTRIES PER CATEGORY")
category_counts = df.groupby("category").size()
print(category_counts.to_string())


# ----------------------------- Q6 ---------------------------------
def score_hypothesis_with_ties(query, dataframe=df):
    """
    Return all entries with the highest matching confidence.
    Unlike a single-result search, this function keeps every tied result.
    """
    results = score_hypothesis(query, dataframe)

    if not results:
        return []

    highest_score = results[0]["score"]
    return [
        result for result in results
        if abs(result["score"] - highest_score) < 1e-12
    ]


print("\\n" + "=" * 65)
print("Q6: HYPOTHESIS SCORING WITH TIE HANDLING")

# 'fee' is present in both fixed billing entries, giving a tie:
# each entry matches one keyword out of four (confidence = 0.25).
tie_query = "fee"
tie_results = score_hypothesis_with_ties(tie_query)

print(f"\\nTie demonstration query: '{tie_query}'")
if tie_results:
    print("All entries sharing the highest score:")
    for result in tie_results:
        print(
            f"- {result['question']} "
            f"(score: {result['score']:.2f}, "
            f"matched: {result['matched_keywords']})"
        )
else:
    print("No matching FAQ entry found.")

# A query that produces a single highest-scoring entry.
non_tie_query = "password reset login"
non_tie_results = score_hypothesis_with_ties(non_tie_query)

print(f"\\nNon-tie demonstration query: '{non_tie_query}'")
if non_tie_results:
    print("Highest-scoring entry/entries:")
    for result in non_tie_results:
        print(
            f"- {result['question']} "
            f"(score: {result['score']:.2f})"
        )
else:
    print("No matching FAQ entry found.")

print("\\nAssignment questions Q1-Q6 completed.")
