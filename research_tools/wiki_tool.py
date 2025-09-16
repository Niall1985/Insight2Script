import wikipedia

def extract_wiki_data(topic):
    page_content = ""
    wikipedia.set_lang("en")
    page = wikipedia.page(topic, auto_suggest=False)
    page_content += page.content
    return page_content

# if __name__ == "__main__":
#     page_content = extract_wiki_data("Nikola Tesla")
#     print(page_content)

