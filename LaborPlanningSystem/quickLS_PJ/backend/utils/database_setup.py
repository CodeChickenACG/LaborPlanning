from pymongo import MongoClient
from datetime import datetime, timedelta

# MongoDB Atlas connection string (Ensure security in production)
MONGO_URI = "[YOUR MONGODB URI]"

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["LaborPlanningDB"]


def get_associates_collection():
    """Returns the associates collection"""
    return db["associates"]


def get_temp_changes_collection():
    """Returns the temporary changes collection with TTL index"""
    temp_changes = db["temp_changes"]

    # Create TTL index if it doesn't exist (auto-expire after 72 hours)
    if "expires_at_1" not in temp_changes.index_information():
        temp_changes.create_index("expires_at", expireAfterSeconds=259200)  # 72 hours

    return temp_changes


def seed_database():
    """Seed example data if it doesn't exist"""
    associates = get_associates_collection()
    temp_changes = get_temp_changes_collection()

    # Seed associates
    example_aa_data = [
        {"login_id": "A123456", "name": "John Doe", "permissions": ["Stow", "TTB"]},
        {"login_id": "A789012", "name": "Jane Smith", "permissions": ["Pick", "Pack"]},
        {"login_id": "A345678", "name": "Alice Brown", "permissions": ["TTB", "Pack"]},
        {"login_id": "A901234", "name": "Bob White", "permissions": ["Stow", "Pick"]}
    ]

    for aa in example_aa_data:
        if not associates.find_one({"login_id": aa["login_id"]}):
            associates.insert_one(aa)
            print(f"Inserted: {aa['name']}")
        else:
            print(f"Skipped (Already Exists): {aa['name']}")

    # Seed temporary changes example
    example_temp_change = {
        "login_id": "A999999",
        "change_type": "add",
        "permissions": ["ProblemSolve"],
        "requested_by": "PA_Jane",
        "expires_at": datetime.utcnow() + timedelta(hours=72),
        "status": "pending"
    }

    if not temp_changes.find_one({"login_id": "A999999"}):
        temp_changes.insert_one(example_temp_change)
        print("Inserted example temporary change")


def get_temp_changes_collection():
    """Returns the temporary changes collection with TTL index"""
    temp_changes = db["temp_changes"]

    try:
        if "expires_at_1" not in temp_changes.index_information():
            temp_changes.create_index("expires_at", expireAfterSeconds=259200)
    except Exception as e:
        print(f"TTL index creation failed: {str(e)}")
        print("Ensure your database user has 'dbAdmin' privileges")

    return temp_changes


if __name__ == "__main__":
    # Verify collections exist
    print("Collections in database:", db.list_collection_names())

    # Verify indexes
    temp_changes = get_temp_changes_collection()
    print("TTL Indexes:", temp_changes.index_information())

    # Seed data
    seed_database()
