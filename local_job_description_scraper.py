'''
Job description scraper
the idea is to replicate the same script that call OpenAI API
but this time, we'll run an Ollama model in the local  machine.
So no uploading no data to the cloud, all computations are performed locally.

'''

## imports
import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
# !ollama pull llama3.2
## constants
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"
url = "https://eeho.fa.us2.oraclecloud.com/hcmUI/CandidateExperience/en/sites/jobsearch/job/275190"

class Website:
	def __init__(self,url):
		'''
		Create this website object from the given URL using the BeautifulSoup Library

		'''
		self.url = url
		response = requests.get(url, headers=HEADERS)
		soup = BeautifulSoup(response.content, 'html.parser') ## parse out website text
		self.title = soup.title.string if soup.title else 'No title found'
		for irrelevant in soup.body(["script", "style", "img", "input"]):
			irrelevant.decompose()
		self.text = soup.body.get_text(separator='\n', strip=True)

system_prompt = "You are an assistant that analyzes the contents of a website \
identifies a job description, and highlights the top 8 skills for the job description, skills, responsibilities, and qualifications; \
ignore text that is not related to the job description, also that might be navigation related. \
Respond in markdown. "


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
	"role": "user", "content": user_prompt_for(Website(url))}
	]

payload = {
	"model": MODEL,
	"messages": messages_for(url),
	"stream": False
}

def scrape_jd(url):
	jd = Website(url)
	response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
	return response.json()['message']['content']

def display_summary(url):
	new_resume = scrape_jd(url)
	display(Markdown(new_resume))
	with open('ollama_resume.md', 'w') as file:
		file.write(new_resume)

display_summary(url)