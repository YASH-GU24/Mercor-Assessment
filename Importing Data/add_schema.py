# importing required libraries
import weaviate
import pandas as pd
from datetime import datetime
import re

# setting up client
client = weaviate.Client("http://localhost:8080")

# creating the schema
candidate_class_schema = {
    "classes": [
        {
            "class": "MercorUsers",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text",
                }
            },
            "properties": [
                {"name": "userId", "dataType": ["string"]},
                {"name": "email", "dataType": ["string"]},
                {"name": "name", "dataType": ["string"]},
                {"name": "phone", "dataType": ["string"]},
                {"name": "residence", "dataType": ["string"]},
                {"name": "profilePic", "dataType": ["string"]},
                {"name": "createdAt", "dataType": ["text"]},
                {"name": "lastLogin", "dataType": ["text"]},
                {"name": "notes", "dataType": ["text"]},
                {"name": "referralCode", "dataType": ["string"]},
                {"name": "isGptEnabled", "dataType": ["number"]},
                {"name": "preferredRole", "dataType": ["string"]},
                {"name": "fullTimeStatus", "dataType": ["string"]},
                {"name": "workAvailability", "dataType": ["string"]},
                {"name": "fullTimeSalaryCurrency", "dataType": ["string"]},
                {"name": "fullTimeSalary", "dataType": ["number"]},
                {"name": "partTimeSalaryCurrency", "dataType": ["string"]},
                {"name": "partTimeSalary", "dataType": ["number"]},
                {"name": "fullTime", "dataType": ["number"]},
                {"name": "fullTimeAvailability", "dataType": ["number"]},
                {"name": "partTime", "dataType": ["number"]},
                {"name": "partTimeAvailability", "dataType": ["number"]},
                {"name": "w8BenUrl", "dataType": ["string"]},
                {"name": "tosUrl", "dataType": ["string"]},
                {"name": "policyUrls", "dataType": ["string"]},
                {"name": "isPreVetted", "dataType": ["number"]},
                {"name": "isActive", "dataType": ["number"]},
                {"name": "isComplete", "dataType": ["number"]},
                {"name": "summary", "dataType": ["text"]},
                {"name": "preVettedAt", "dataType": ["text"]},
            ],
        },
        {
            "class": "UserResume",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text",
                }
            },
            "properties": [
                {"name": "resumeId", "dataType": ["string"]},
                {"name": "url", "dataType": ["string"]},
                {"name": "filename", "dataType": ["string"]},
                {"name": "createdAt", "dataType": ["text"]},
                {"name": "updatedAt", "dataType": ["text"]},
                {"name": "source", "dataType": ["string"]},
                {"name": "ocrText", "dataType": ["text"]},
                {"name": "ocrEmail", "dataType": ["string"]},
                {"name": "ocrGithubUsername", "dataType": ["string"]},
                {"name": "resumeBasedQuestions", "dataType": ["text"]},
            ],
        },
        {
            "class": "Education",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text",
                }
            },
            "properties": [
                {"name": "educationId", "dataType": ["string"]},
                {"name": "degree", "dataType": ["string"]},
                {"name": "major", "dataType": ["string"]},
                {"name": "school", "dataType": ["string"]},
                {"name": "startDate", "dataType": ["text"]},
                {"name": "endDate", "dataType": ["text"]},
                {"name": "grade", "dataType": ["string"]},
            ],
        },
        {
            "class": "WorkExperience",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text",
                }
            },
            "properties": [
                {"name": "workExperienceId", "dataType": ["string"]},
                {"name": "company", "dataType": ["string"]},
                {"name": "role", "dataType": ["string"]},
                {"name": "startDate", "dataType": ["text"]},
                {"name": "endDate", "dataType": ["text"]},
                {"name": "description", "dataType": ["text"]},
                {"name": "locationCity", "dataType": ["string"]},
                {"name": "locationCountry", "dataType": ["string"]},
            ],
        },
        {
            "class": "PersonalInformation",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text",
                }
            },
            "properties": [
                {"name": "personalInformationId", "dataType": ["string"]},
                {"name": "name", "dataType": ["string"]},
                {"name": "location", "dataType": ["string"]},
                {"name": "email", "dataType": ["string"]},
                {"name": "phone", "dataType": ["string"]},
            ],
        },
        {
            "class": "Skills",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text",
                }
            },
            "properties": [
                {"name": "skillId", "dataType": ["string"]},
                {"name": "skillName", "dataType": ["string"]},
                {"name": "skillValue", "dataType": ["string"]},
            ],
        },
        {
            "class": "MercorUserSkills",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text",
                }
            },
            "properties": [
                {
                    "name": "userId",
                    "dataType": ["text"],
                    "description": "Reference to MercorUsers",
                },
                {
                    "name": "skillId",
                    "dataType": ["text"],
                    "description": "Reference to Skills",
                },
                {"name": "isPrimary", "dataType": ["number"]},
                {"name": "order", "dataType": ["number"]},
            ],
        },
    ]
}
for cls in candidate_class_schema["classes"]:
    client.schema.delete_class(cls["class"])
    client.schema.create_class(cls)
