from flask import Flask, make_response, jsonify, request
from flask_cors import CORS
from flask_mongoengine import MongoEngine
import linkedin_automated_scraper
import time
from mongoengine import Document, ListField, StringField, URLField
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

username = os.environ.get('MONGODB_USERNAME')
password = os.environ.get('MONGODB_PASSWORD')
dbname = os.environ.get('MONGODB_DBNAME')
linkedin_url = os.environ.get('LINKEDIN_URL')

app = Flask(__name__)
CORS(app)
app.config['MONGODB_SETTINGS'] = {
	'host':'mongodb+srv://{}:{}@{}.vmrhn7r.mongodb.net/?retryWrites=true&w=majority'.format(username, password, dbname)
}
db = MongoEngine(app)
# db.init_app(app)

class Job(db.Document):
    job_id = db.StringField(required=True, unique = True, )
    title = db.StringField(required=True)
    company = db.StringField(required=True)
    company_thumbnail = db.URLField()
    tags = db.ListField(StringField())

@app.route('/test')
def test():
    return make_response({'new_jobs':5}, 200)
 
@app.route('/modify_tags/<string:id>', methods=['POST'])
def modify_job_tags(id):
    print(request.json)
    body = request.json
    job = Job.objects(job_id=id)[0]
    job.tags = body['tags']
    job.save()
    return make_response({'new_tags':body['tags']}, 200)
    
@app.route('/delete_all', methods=['DELETE'])
def delete_all_jobs():
    try:
        for job in Job.objects():
            job.delete()
        return make_response('all jobs deleted', 200)
    except Exception as e:
        return make_response('error deleting saved jobs', 200)
    

@app.route('/extract_saved_jobs', methods=['GET'])
def extract_saved_jobs():
    try:
        saved_jobs_list = linkedin_automated_scraper.extract_all_saved_jobs()
        print(len(saved_jobs_list))
        number_of_new_saved_jobs = 0
        for saved_job in saved_jobs_list:
            if saved_job['job_id'] not in list(map(lambda x: x['job_id'], Job.objects())):
                job = Job(
		    job_id = saved_job['job_id'],
		    title = saved_job['title'],
		    company = saved_job['company'],
		    company_thumbnail = saved_job['company_thumbnail'],
		    tags = []
            	)
                job.save()
                number_of_new_saved_jobs += 1
        return make_response({'new_jobs':number_of_new_saved_jobs}, 200)
    except Exception as e:
        print('error retrieving jobs:\n {}'.format(e))
        return make_response('error retrieving jobs:\n {}'.format(e), 500)

@app.route('/jobs', methods=['GET'])
def get_jobs():
    try:
        jobs = []
        for job in Job.objects():
            print('{}, {}, {}'.format(job.job_id, job.title, job.company))
            jobs.append({
            'id':job.job_id,
            'link' : '{}/{}'.format(linkedin_url, job.job_id),
            'title' :  job.title,
            'company' : job.company,
            'company_thumbnail' : job.company_thumbnail,
            'tags' : [tag for tag in job.tags]
            })
        return make_response(jsonify(jobs), 200)
    except Exception as e:
        print(e)
        return make_response('Error retrieving jobs!', 500)


if __name__ =="__main__":
    app.run()
