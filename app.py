from flask import Flask, make_response
from flask_cors import CORS
import linkedin_automated_scraper
import time
from db import Job

app = Flask(__name__)
CORS(app)
connect('project1')

@app.route('/')
def test():
    return make_response('app running!!', 200)

@app.route('/extract_saved_jobs')
def extract_saved_jobs():
    try:
        saved_jobs_list = linkedin_automated_scraper.extract_all_saved_jobs()
        for saved_job in saved_jobs_list:
            job = Job()
            Job.save()
        return make_response('jobs extracted', 200)
    except Exception as e:
        print(e)
        return make_response('error retrieving jobs', 500)

@app.route('/jobs', methods=['GET'])
def get_jobs():
    try:
        jobs = []
        for job in Job.objects:
            jobs.append({
            link = 'https://www.linkedin.com/jobs/view/{}'.format(job.job_id),
            title = job.title,
            company = job.company,
            company_thumbnail = job.company_thumbnail,
            tags = [tag for tag in job.tags]
            })
        return make_response(jobs, 200)
   except Exception as e:
       print(e)
       return make_response('Error retrieving jobs!', 500)


if __name__ =="__main__":
    app.run()
