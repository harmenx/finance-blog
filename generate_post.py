import os
import sys
import datetime
from openai import OpenAI
import re
from dotenv import load_dotenv

load_dotenv()

def generate_post_content(topic, poe_api_key):
    prompt = f"""
Generate a high-value, SEO-friendly blog post about "{topic}".
The post should be approximately 800-1200 words and follow this structure:

1.  **Catchy Title:** A compelling and SEO-optimized title.
2.  **Introduction:** Hook the reader, briefly introduce the topic, and state what they will learn.
3.  **Main Body (3-5 sections):
    *   Each section should cover a specific aspect of the topic.
    *   Use clear headings and subheadings (H2, H3).
    *   Provide actionable insights, explanations, and examples.
    *   Incorporate relevant keywords naturally throughout the text.
4.  **Conclusion:** Summarize key takeaways, offer a final thought, and a call to action.
5.  **SEO Description:** A concise, compelling summary (around 150-160 characters) for search engines.

Please provide the output in Markdown format.
Also, suggest 2-3 relevant categories and 5-7 relevant tags for the post.
"""
    client = OpenAI(
        api_key=poe_api_key,
        base_url="https://api.poe.com/v1"
    )
    
    completion = client.chat.completions.create(
        model="gpt-4", 
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
    )

    return completion.choices[0].message.content

def create_jekyll_post(topic, content):
    # Extract title, SEO description, categories, and tags from the generated content
    title_match = re.search(r"^(?:Catchy )?Title:\s*(.*)", content, re.IGNORECASE | re.MULTILINE)
    title = title_match.group(1).strip() if title_match else topic.replace("-", " ").title()

    seo_description_match = re.search(r"^(?:SEO )?Description:\s*(.*)", content, re.IGNORECASE | re.MULTILINE)
    seo_description = seo_description_match.group(1).strip() if seo_description_match else f"A blog post about {topic}."

    categories_match = re.search(r"^Categories:\s*(.*)", content, re.IGNORECASE | re.MULTILINE)
    categories = [c.strip() for c in categories_match.group(1).split(',') if c.strip()] if categories_match else ["uncategorized"]

    tags_match = re.search(r"^Tags:\s*(.*)", content, re.IGNORECASE | re.MULTILINE)
    tags = [t.strip() for t in tags_match.group(1).split(',') if t.strip()] if tags_match else ["blog"]

    # Clean up content by removing the extracted parts
    content = re.sub(r"^(?:Catchy )?Title:.*\n?", "", content, flags=re.IGNORECASE | re.MULTILINE)
    content = re.sub(r"^(?:SEO )?Description:.*\n?", "", content, flags=re.IGNORECASE | re.MULTILINE)
    content = re.sub(r"^Categories:.*\n?", "", content, flags=re.IGNORECASE | re.MULTILINE)
    content = re.sub(r"^Tags:.*\n?", "", content, flags=re.IGNORECASE | re.MULTILINE)
    content = content.strip()

    # Generate filename
    today = datetime.datetime.now()
    filename_date = today.strftime("%Y-%m-%d")
    filename_title = re.sub(r"[^a-zA-Z0-9]+", "-", title.lower()).strip("-")
    filename = f"{filename_date}-{filename_title}.md"

    # Construct front matter
    front_matter = f"""
---
layout: post
title: \"{title}\" 
date: {today.strftime("%Y-%m-%d %H:%M:%S %z")}
categories: {categories}
tags: {tags}
seo_title: \"{title}\" 
description: \"{seo_description}\" 
---

"""
    return filename, front_matter + content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_post.py \"Your Blog Post Topic\"")
        sys.exit(1)

    blog_topic = sys.argv[1]
    poe_api_key = os.getenv("POE_API_KEY")

    if not poe_api_key:
        print("Error: POE_API_KEY environment variable not set.")
        sys.exit(1)

    print(f"Generating post for topic: {blog_topic}")
    try:
        generated_content = generate_post_content(blog_topic, poe_api_key)
        filename, full_content = create_jekyll_post(blog_topic, generated_content)

        posts_dir = "_posts"
        os.makedirs(posts_dir, exist_ok=True)
        filepath = os.path.join(posts_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"Successfully created post: {filepath}")
    except Exception as e:
        print(f"An error occurred during post generation: {e}")
        sys.exit(1)
