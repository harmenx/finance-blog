# Crypto Finance Education Blog

This project sets up an automated blog for generating high-value, SEO-friendly content related to cryptocurrency, finance, and making money. It leverages Poe for content generation, Jekyll for static site generation, and GitHub Actions for continuous automation and deployment to GitHub Pages.

## Features

*   **Modern & Responsive Design:** A clean, dark-themed, and mobile-friendly design that looks great on all devices.
*   **Automated Content Generation:** Generates blog posts using the Poe API based on predefined topics and structures.
*   **SEO-Friendly:** Content is designed to be SEO-optimized with catchy titles, descriptions, categories, and tags.
*   **Jekyll Integration:** Generated posts are formatted as Jekyll Markdown files with appropriate front matter.
*   **GitHub Pages Deployment:** Automatically builds and deploys the blog to GitHub Pages via GitHub Actions.
*   **Daily Posting:** Configured to generate 1-2 new posts daily.

## Local Development

To set up the blog for local development, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/crypto-finance-education-blog.git
cd crypto-finance-education-blog
```

### 2. Set Up Poe API Key

Create a `.env` file in the root of the project and add your Poe API key:

```
POE_API_KEY=YOUR_POE_API_KEY_HERE
```

**Remember to replace `YOUR_POE_API_KEY_HERE` with your actual Poe API key.**

### 3. Install Dependencies

*   **Python:** Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

*   **Jekyll:** Install Jekyll and the bundler gem:

    ```bash
    gem install bundler jekyll
    ```

### 4. Run the Jekyll Server

Start the Jekyll server to view the blog locally:

```bash
bundle exec jekyll serve
```

The blog will be available at `http://localhost:4000`.

## Usage

### Local Content Generation

You can generate a single blog post locally using the `generate_post.py` script:

```bash
python generate_post.py "Your Desired Blog Post Topic"
```

This will create a new Markdown file in the `_posts` directory.

### Automated Workflows (GitHub Actions)

This project uses two separate GitHub Actions workflows:

*   **`generate-post.yml`:** This workflow runs on a schedule (daily at 10:00 UTC) or can be triggered manually. It generates new blog posts using the `generate_post.py` script and commits them to the repository.
*   **`build.yml`:** This workflow is triggered on every push to the `main` branch. It builds the Jekyll site and deploys it to GitHub Pages.

To trigger a manual run of the `generate-post` workflow:

1.  Go to your repository on GitHub.
2.  Click on the "Actions" tab.
3.  Select the "Generate New Posts" workflow.
4.  Click "Run workflow" and then "Run workflow" again to confirm.

## Project Structure

*   `_posts/`: Contains the generated Jekyll blog posts.
*   `.github/workflows/`: Contains the GitHub Actions workflows.
    *   `generate-post.yml`: Workflow for generating new posts.
    *   `build.yml`: Workflow for building and deploying the site.
*   `generate_post.py`: Python script for generating blog post content via Poe.
*   `requirements.txt`: Python dependencies.
*   `.env`: Local environment variables (ignored by Git).
*   `README.md`: This file.
