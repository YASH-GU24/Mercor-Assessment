# importing required libraries
import weaviate
import pandas as pd
from datetime import datetime
import json

# setting up client
client = weaviate.Client("http://localhost:8080")

client.schema.property.create(
    "MercorUsers", {"name": "has_resume", "dataType": ["UserResume"]}
)

client.schema.property.create(
    "UserResume", {"name": "has_education", "dataType": ["Education"]}
)

client.schema.property.create(
    "UserResume", {"name": "has_work_experience", "dataType": ["WorkExperience"]}
)


client.schema.property.create(
    "UserResume",
    {"name": "has_personal_information", "dataType": ["PersonalInformation"]},
)

client.schema.property.create(
    "MercorUsers", {"name": "has_skills", "dataType": ["MercorUserSkills"]}
)


client.schema.property.create(
    "MercorUserSkills", {"name": "has_skill_detail", "dataType": ["Skills"]}
)
