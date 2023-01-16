from mongoengine import Document, ListField, StringField, URLField

class Job(Document):
    job_id = StringField(required=True)
    title = StringField(required=True)
    company = StringField(required=True)
    company_thumbnail = URLField()
    tags = ListField(StringField(max_length=20))
