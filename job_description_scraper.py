'''
LLM implementation of web scraping.
The goal here is to scrape a website with a job description
and tailor my resume to the job description at hand
'''

# imports
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI

## load environment variables in a filled called .env - for OpenAI billing
load_dotenv(override=True)
api_key = os.getenv('OpenAI_API_KEY')
openai = OpenAI()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
### create website class
class Website:
	def __init__(self,url):
		'''
		Create this website object from the given URL using the BeautifulSoup Library

		'''
		self.url = url
		response = requests.get(url, headers=headers)
		soup = BeautifulSoup(response.content, 'html.parser') ## parse out website text
		self.title = soup.title.string if soup.title else 'No title found'
		for irrelevant in soup.body(["script", "style", "img", "input"]):
			irrelevant.decompose()
		self.text = soup.body.get_text(separator='\n', strip=True)

system_prompt = "You are an assistant that analyzes the contents of a website \
identifies a job description, and highlights the top 8 skills for the job description, skills, responsibilities, and qualifications; \
ignore text that is not related to the job description, also that might be navigation related. \
Respond in markdown. "


### function for writing a user prompt that tailors resume to highlights of the website's job description
def user_prompt_for(website):
	user_prompt = f"You are looking at a website titled {website.title}"
	user_prompt += "My current resume is as follows:\
		EXPERIENCE \
		Data Scientist in Infant Epidemiology| Seattle Children’s Hospital\
		June 2022 - Present\
		●	Developed and deployed machine learning models at scale for academic research of health\
		●	Applied advanced statistical techniques and deep learning for data classification\
		●	Implemented predictive models for estimating quantitative variables \
		●	Managed large-scale data processing pipelines using cloud technologies\
		●	Collaborated with cross-functional teams to integrate computational and clinical perspectives\
		●	Created data visualization and cohesive presentations at various conferences, showcasing ability to summarize research highlights in a cohesive and coherent manner.\
		Data Science Intern | Zero-g space\
		January 2023 - June 2023\
		●	Developed and deployed computer vision models for detecting shapes within images\
		●	Applied advanced statistical techniques including deep learning for data classification\
		●	Implemented and deployed custom computer vision algorithms to assess object sizes in images\
		●	Developed pilot versions of data analysis pipelines for supervised machine learning training and testing\
		●	Created visualization dashboards for internal company communication\
		●	Applied science research with applications in aerospace industry\
		Research Assistant | Emory University\
		March 2018 - April 2022\
		●	Developed and deployed optimization of computational models of neural dynamics controlling neuronal activity\
		●	Employed state-of-the-art brain-machine-interface prototypes for academic research\
		●	Implemented Machine Learning pipelines for classification of neuronal data\
		●	Presented research findings in multiple academic contexts: manuscripts, tutorials, conferences\
		●	Outstanding publication track record: one experimental tutorial hosted at Journal of Visualized experiments, two academic publications in eNeuro and Physical Review E; showcasing ability to communicate research findings.\
		Graduate Research Assistant | Georgia State University\
		August 2015 - March 2018\
		●	Specialized in computational modeling of physical and biophysical phenomena such as activity propagation, rhythmicity, learning, and neuromodulation.\
		●	Developed analytical techniques to understand neuronal communication, relevant for academic research\
		●	Implemented neural networks for computer vision and machine learning\
		●	Collaborated with researchers from different fields, highlighting my capacity to collaborate, coordinate, and communicate with people of various backgrounds\
		●	Extensive training in computer science and coding in various languages: Python, Matlab, C\
		●	Training in data visualization techniques using custom tools from Python, Matplotlib, and Matlab.\
		SKILLS\
		Machine Learning & AI\
		1.	Advanced ML model development and deployment\
		2.	Deep learning and neural networks\
		3.	Basic LLM implementation and fine-tuning\
		4.	Natural language processing fundamentals\
		Programming & Tools\
		5.	Languages: Python, PyTorch, C++, Matlab, C\
		6.	Cloud Platforms: AWS, Azure, GCP, Linux-based computer cluters\
		7.	MLOps: MLflow, CI/CD pipelines\
		8.	Data Visualization: Matplotlib & Seaborn\
		Soft Skills\
		9.	Agile methodology\
		10.	Cross-functional collaboration\
		11.	Technical documentation\
		12.	Research communication\
		13.	Ability to teach and explain complex science and math topics in laymen terms\
		 end of resume\
		Now please modify this resume, highlighting relevant skills and experience\
		based on the highlighted skills and experiences."
	user_prompt += website.text
	return user_prompt
### function for creating the messages for the OpenAI API
def messages_for(website):
	return [
	{"role": "system", "content": system_prompt,
	"role": "user", "content": user_prompt_for(website)}
	]


jd = Website("https://eeho.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/jobsearch/job/275190")
# user_prompt_for(jd)
# messages_for(jd)

def scrape_jd(url):
	jd = Website(url)
	response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages_for(jd))
	return response.choices[0].message.content

def display_summary(url):
	new_resume = scrape_jd(url)
	display(Markdown(new_resume))
	with open('new_resume.md', 'w') as file:
		file.write(new_resume)

display_summary("https://eeho.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/jobsearch/job/275190")