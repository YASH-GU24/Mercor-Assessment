import mysql.connector
import pandas as pd
from mysql.connector import Error
import weaviate
from weaviate.auth import AuthClientPassword
import uuid
import hashlib


def generate_uuid_from_two_uuids(uuid1, uuid2):
    # Convert UUIDs to strings
    uuid1_str = str(uuid1)
    uuid2_str = str(uuid2)

    # Concatenate the two UUID strings
    combined_str = uuid1_str + uuid2_str

    # Generate a hash of the combined string
    hash_obj = hashlib.sha256(combined_str.encode())

    # Get the first 32 hexadecimal characters of the hash
    hash_hex = hash_obj.hexdigest()[:32]

    # Create a new UUID from the hash
    new_uuid = uuid.UUID(hash_hex)

    return new_uuid


# Database connection details
db_config = {
    "host": "35.224.61.48",
    "port": 3306,
    "database": "MERCOR_TRIAL_SCHEMA",
    "user": "trial_user",
    "password": "trial_user_12345#",
}

# Weaviate connection details
weaviate_config = {
    "url": "http://localhost:8080",  # Change to your Weaviate instance URL
    "username": "your_username",  # If needed
    "password": "your_password",  # If needed
    "scope": "offline_access",  # If needed
}


# Function to get MySQL connection
def get_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


# Function to convert pandas.Timestamp to RFC 3339 format
def timestamp_to_rfc3339(timestamp):
    return timestamp.isoformat()


# Function to get data from a MySQL table
def get_table_data(table_name):
    connection = get_connection()
    if connection is None:
        return None
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, connection)
    connection.close()
    return df


# Function to convert timestamps in dataframe to RFC 3339
def convert_timestamps(df, timestamp_columns):
    for column in timestamp_columns:
        if column in df.columns:
            df[column] = df[column].apply(
                lambda x: timestamp_to_rfc3339(x)
                if pd.notnull(x) and type(x) is not str
                else x
            )
    return df


# Function to replace NaN values
def replace_nan_values(df, replace_with=""):
    return df.fillna(replace_with)


# Function to convert specific columns to float
def convert_to_float(df, float_columns):
    for column in float_columns:
        if column in df.columns:
            df[column] = df[column].replace("", 0)
            df[column] = df[column].astype(float)
    return df


# Function to upload data to Weaviate
def upload_to_weaviate(weaviate_client, class_name, data):
    for i, row in data.iterrows():
        print("Added to table " + class_name + " " + str(i))
        properties = row.to_dict()
        try:
            if class_name == "UserResume":
                weaviate_client.data_object.reference.add(
                    from_class_name="MercorUsers",
                    from_uuid=properties["userId"],
                    from_property_name="has_resume",
                    to_class_name="UserResume",
                    to_uuid=properties["resumeId"],
                )
        except Exception as err:
            print("ERR: ", err)
        if class_name == "MercorUserSkills":
            weaviate_client.data_object.reference.add(
                from_class_name="MercorUsers",
                from_uuid=properties["userId"],
                from_property_name="has_skills",
                to_class_name="MercorUserSkills",
                to_uuid=generate_uuid_from_two_uuids(
                    properties["skillId"], properties["userId"]
                ),
            )
            weaviate_client.data_object.reference.add(
                from_class_name="MercorUserSkills",
                from_uuid=generate_uuid_from_two_uuids(
                    properties["skillId"], properties["userId"]
                ),
                from_property_name="has_skill_detail",
                to_class_name="Skills",
                to_uuid=properties["skillId"],
            )
        if class_name == "Education":
            if properties["educationId"] != "":
                weaviate_client.data_object.reference.add(
                    from_class_name="UserResume",
                    from_uuid=properties["resumeId"],
                    from_property_name="has_education",
                    to_class_name="Education",
                    to_uuid=properties["educationId"],
                )
        if class_name == "WorkExperience":
            if properties["workExperienceId"] != "":
                weaviate_client.data_object.reference.add(
                    from_class_name="UserResume",
                    from_uuid=properties["resumeId"],
                    from_property_name="has_work_experience",
                    to_class_name="WorkExperience",
                    to_uuid=properties["workExperienceId"],
                )
        if class_name == "PersonalInformation":
            if properties["personalInformationId"] != "":
                weaviate_client.data_object.reference.add(
                    from_class_name="UserResume",
                    from_uuid=properties["resumeId"],
                    from_property_name="has_personal_information",
                    to_class_name="PersonalInformation",
                    to_uuid=properties["personalInformationId"],
                )


# Main function to extract and upload data
def main():
    # Initialize Weaviate client
    client = weaviate.Client(
        weaviate_config["url"],
        auth_client_secret=AuthClientPassword(
            username=weaviate_config["username"],
            password=weaviate_config["password"],
            scope=weaviate_config["scope"],
        ),
    )

    # Define tables and their timestamp and float columns
    tables = {
        "MercorUsers": {
            "timestamp_columns": ["createdAt", "lastLogin"],
            "float_columns": [
                "partTimeSalary",
                "fullTimeSalary",
                "partTimeAvailability",
                "fullTimeAvailability",
            ],
        },
        "UserResume": {
            "timestamp_columns": ["createdAt", "updatedAt"],
            "float_columns": [],
        },
        "Education": {
            "timestamp_columns": ["startDate", "endDate"],
            "float_columns": [],
        },
        "WorkExperience": {
            "timestamp_columns": ["startDate", "endDate"],
            "float_columns": [],
        },
        "PersonalInformation": {"timestamp_columns": [], "float_columns": []},
        "MercorUserSkills": {"timestamp_columns": [], "float_columns": ["isPrimary"]},
        "Skills": {"timestamp_columns": [], "float_columns": []},
    }

    # Extract and upload data for each table
    for table, columns in tables.items():
        data = get_table_data(table)
        if data is not None:
            data = replace_nan_values(data)
            data = convert_timestamps(data, columns["timestamp_columns"])
            data = convert_to_float(data, columns["float_columns"])
            upload_to_weaviate(client, table, data)
        else:
            print(f"Failed to retrieve data for table: {table}")


if __name__ == "__main__":
    main()
