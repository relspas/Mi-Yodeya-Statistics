import requests

books = ["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy"]
base_url = "https://www.sefaria.org/api/v3/texts/Rashi on {}"

longest_rashi = {"book": "", "ref": "", "text": "", "word_count": 0}

for book in books:
    url = base_url.format(book)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching {book}")
        continue

    data = response.json()
    text = data["versions"][0]["text"]  # This is a 3-level nested list: [chapters][verses][comments]

    for chapter_index, chapter in enumerate(text):
        for verse_index, verse in enumerate(chapter):
            for comment_index, comment in enumerate(verse):
                # Remove tags and extra whitespace
                clean_comment = comment.replace("<b>", "").replace("</b>", "").strip()
                word_count = len(clean_comment.split())

                if word_count > longest_rashi["word_count"]:
                    longest_rashi = {
                        "book": book,
                        "ref": f"{book} {chapter_index+1}:{verse_index+1} (Comment {comment_index+1})",
                        "text": clean_comment,
                        "word_count": word_count
                    }

print("📜 Longest Rashi in the Torah")
print(f"📖 Location: {longest_rashi['ref']}")
print(f"🔢 Word count: {longest_rashi['word_count']}")
print(f"📝 Text:\n{longest_rashi['text']}")
