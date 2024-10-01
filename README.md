# CoverLetterGPT: Your Automated Job Application Assistant

Welcome to **CoverLetterGPT**, a tool to search jobs on Linkedin and automated cover letter writer to simplify your job search! Tired of writing repetitive cover letters? I hope that this tool can save you some time landing your dream job. 

Brace yourself! This app is designed to be **super intuitive**—even if you’re not into coding, you’ll find it easy to use. Let's dive in!

---

## ⚠️ Important Notes (Read First!)

- **API Costs**: Be cautious about which model you use in OpenAI's API. Some models are cheap, but others can add up quickly! Always keep track of your usage. [Check pricing here](https://openai.com/api/pricing/).
- **Privacy**: Your LinkedIn cookie is stored securely, but make sure you **never** share your `.env` file with anyone. If you leak your API key, other people might use your credits.
- **Responsible Usage**: I am **in no way responsible** for any illicit or irresponsible use of this repository or the LinkedIn scraper. Make sure to follow LinkedIn's terms of service when using this tool.

---

## 💡 How Does It Work?

**CoverLetterGPT** uses OpenAI's GPT technology to craft personalized cover letters for job applications, but how is it different from using ChatGPT directly? Simple! With **CoverLetterGPT**, you'll save time by skipping repetitive tasks. This tool automates the process by fetching job details from LinkedIn, generating tailored cover letters instantly, so you can focus on applying instead of rewriting.

The app leverages code from [streamlit-linkedin-jobs](https://github.com/shabpompeiano/streamlit-linkedin-jobs) for the Streamlit app and incorporates components from [py-linkedin-jobs-scraper](https://github.com/spinlud/py-linkedin-jobs-scraper) to scrape LinkedIn job data.

---

## 🎯 Features
- **Automated Cover Letters**: Personalized to the job description and your experience.
- **LinkedIn Integration**: Fetch jobs and craft cover letters from listings directly.
- **Customizable**: You can tweak the cover letters to match your tone. You can also chat with the cover letters to iteratively fix them.

---

## 🛠️ Setup Guide (No Coding Skills Needed)

### 1. **Get Your OpenAI API Key**
- Sign up for an API key at OpenAI: [Get API Key](https://openai.com/index/openai-api/)
- **Heads up**: This API, as most, isn't free. The cost depends on the model you use, but don’t worry—there are cheaper models available. Check pricing here: [OpenAI Pricing](https://openai.com/api/pricing/) You will be able to change the model inside the app! **You pay a tiny sum for each interaction with GPT** i.e. with each cover letter generation and chat interaction with this. 
- You’ll be using your key in the `.env` file for secure access.

### 2. **Get Your LinkedIn Cookie**
To allow the app to search jobs for you on LinkedIn, we’ll need your LinkedIn cookie for authentication. Follow this simple guide to obtain your cookie. [Here’s the guide!](https://github.com/spinlud/py-linkedin-jobs-scraper#anonymous-vs-authenticated-session)

### 3. **Fill in Your API Key**
- After getting your OpenAI API key, open the `.env` file (this file holds sensitive info securely).
- Paste your key like this:
  ```
  OPENAI_API_KEY=your-key-here 
  LI_AT_COOKIE=your-linkedin-cookie-here 
  ```

### 4. **Install Requirements**
Now, let’s install what you need to run the app:
- Create a virtual environment (recommended):
  ```
  python3 -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
  ```
- Install dependencies from `requirements.txt`:
  ```
  pip install -r requirements.txt
  ```

### 5. **Run the App**
Now you're all set! Run the Streamlit app with this command:
```
streamlit run Home.py
```

### 6. **You're Ready to Go!**
The app will open in your browser. You can now search jobs on LinkedIn and generate cover letters instantly. Good luck with your job search! 🚀

--- 

## 👨‍💻 Contributions Welcome!

Feel free to contribute to **CoverLetterGPT**! I welcome pull requests from anyone interested in improving the app. Here's a list of things future collaborators can help with:

### TODO List:
- **Add More Retrievers**: Integrate job retrievers for Indeed, Glassdoor, and other job platforms.
- **Add API Cost Counter**: Implement a counter to estimate API expenses. Check out [this post](https://community.openai.com/t/how-to-accurately-get-the-cost-of-each-api-call/578426/2) to learn how to calculate it.
- **Improve Retrieval Speed**: Explore ways to speed up job data retrieval—maybe try different LinkedIn scrapers.

---

**Happy job hunting!** 
