import weaviate
from queries.rerank import get_reranked
# setting up client
client = weaviate.Client("http://localhost:8080")


def generate_or_text(path, value):
    where_filter = {
        "path": path,
        "operator": "Like",
        "valueText": "*" + value.lower() + "*",
    }

    return where_filter


def generate_equal_number(path, value):
    where_filter = {
        "path": path,
        "operator": "Equal",
        "valueNumber": value,
    }

    return where_filter


def generate_lte_number(path, value):
    where_filter = {"path": path, "operator": "LessThanEqual", "valueNumber": value}
    return where_filter


def get_extracted_data(user):
    extracted_data = {
        "userId": user["userId"],
        "name": user["name"],
        "email": user["email"],
        "partTimeSalary": user["partTimeSalary"],
        "fullTimeSalary": user["fullTimeSalary"],
        "fullTime": user["fullTime"],
        "partTime": user["partTime"]
    }
    try:
        extracted_data["skills"] = list(
            {skill["has_skill_detail"][0]["skillName"] for skill in user["has_skills"]}
        )
    except:
        extracted_data["skills"] = []
    try:
        extracted_data["companies"] = list(
            {work["company"] for work in user["has_resume"][0]["has_work_experience"]}
        )
    except:
        extracted_data["companies"] = []
    try:
        extracted_data["work_descriptions"] = list(
            {work["description"] for work in user["has_resume"][0]["has_work_experience"]}
        )
    except Exception:
        extracted_data["work_descriptions"] = []
    return extracted_data


def fetch_results(resp, user_chat_history):
    print(resp)
    where_operands = []
    if resp["budget"] != "" and resp["budget"].lower() != "unlimited":
        if resp["role type"] != "":
            if resp["role type"] == "Full Time":
                path = "fullTimeSalary"
            else:
                path = "partTimeSalary"
        else:
            path = "partTimeSalary"
        where_operands.append(generate_lte_number([path], int(resp["budget"])))
    if len(resp["required skills"]) != 0:
        for skill in resp["required skills"]:
            where_operands.append(
                generate_or_text(
                    [
                        "has_skills",
                        "MercorUserSkills",
                        "has_skill_detail",
                        "Skills",
                        "skillName",
                    ],
                    skill,
                )
            )
    if resp["role type"] == "Full Time":
        where_operands.append(generate_equal_number(["fullTime"], 1))
    elif resp["role type"] == "Part Time":
        where_operands.append(generate_equal_number(["partTime"], 1))

    if len(where_operands) == 0:
        where_filter = {}
    elif len(where_operands) == 1:
        where_filter = where_operands[0]
    else:
        where_filter = {"operator": "And", "operands": where_operands}
    print(where_filter)

    near_text = ""
    for msg in user_chat_history:
        near_text = near_text + msg
    if where_filter:
        response = (
            client.query.get(
                "MercorUsers",
                [
                    "name",
                    "email",
                    "partTimeSalary",
                    "fullTimeSalary",
                    "userId",
                    "fullTime",
                    "partTime",
                    "has_skills { ... on MercorUserSkills { has_skill_detail { ... on Skills {skillName}} } }",
                    "has_resume { ... on UserResume { has_work_experience { ... on  WorkExperience {company}} } }",
                    "has_resume { ... on UserResume { has_work_experience { ... on  WorkExperience {description}} } }",
                ],
            )
            .with_near_text({"concepts": near_text})
            .with_where(where_filter)
            .with_limit(200)
            .do()
        )
    else:
        response = (
            client.query.get(
                "MercorUsers",
                [
                    "name",
                    "email",
                    "partTimeSalary",
                    "fullTimeSalary",
                    "userId",
                    "fullTime",
                    "partTime",
                    "has_skills { ... on MercorUserSkills { has_skill_detail { ... on Skills {skillName}} } }",
                    "has_resume { ... on UserResume { has_work_experience { ... on  WorkExperience {company}} } }",
                    "has_resume { ... on UserResume { has_work_experience { ... on  WorkExperience {description}} } }",
                ],
            )
            .with_near_text({"concepts": near_text})
            .with_limit(200)
            .do()
        )
    results = []
    if response["data"]["Get"]["MercorUsers"]:
        for res in response["data"]["Get"]["MercorUsers"]:
            results.append(get_extracted_data(res))
    results = get_reranked(results, near_text)
    return results
