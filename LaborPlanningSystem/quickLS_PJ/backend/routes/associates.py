from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from backend.utils.database_setup import get_associates_collection, get_temp_changes_collection

# Blueprint for associates routes
associates_bp = Blueprint("associates", __name__)

# Get MongoDB collections
associates_collection = get_associates_collection()
temp_changes_collection = get_temp_changes_collection()


# 📌 Get all associates
@associates_bp.route("/associates", methods=["GET"])
def get_all_associates():
    associates = list(associates_collection.find({}, {"_id": 0}))
    return jsonify(associates), 200


# 📌 Get a single associate by login_id
@associates_bp.route("/associates/<login_id>", methods=["GET"])
def get_associate(login_id):
    associate = associates_collection.find_one({"login_id": login_id}, {"_id": 0})
    if not associate:
        return jsonify({"error": "Associate not found"}), 404
    return jsonify(associate), 200


# 📌 Add a new associate
@associates_bp.route("/associates", methods=["POST"])
def add_associate():
    data = request.get_json()
    if not data or "login_id" not in data or "name" not in data or "permissions" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if associates_collection.find_one({"login_id": data["login_id"]}):
        return jsonify({"error": "Associate already exists"}), 409

    associates_collection.insert_one(data)
    return jsonify({"message": "Associate added successfully"}), 201


# 📌 Update an associate's details
@associates_bp.route("/associates/<login_id>", methods=["PUT"])
def update_associate(login_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    result = associates_collection.update_one({"login_id": login_id}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"error": "Associate not found"}), 404

    return jsonify({"message": "Associate updated successfully"}), 200


# 📌 Delete an associate
@associates_bp.route("/associates/<login_id>", methods=["DELETE"])
def delete_associate(login_id):
    result = associates_collection.delete_one({"login_id": login_id})
    if result.deleted_count == 0:
        return jsonify({"error": "Associate not found"}), 404
    return jsonify({"message": "Associate deleted successfully"}), 200


# 📌 Assign labor endpoint
@associates_bp.route("/assign-labor", methods=["POST"])
def assign_labor():
    data = request.get_json()

    # Validate input
    if "logins" not in data or "requirements" not in data:
        return jsonify({"error": "Missing required fields: logins, requirements"}), 400

    logins = data["logins"]  # List of login IDs (e.g., ["login1", "login2"])
    requirements = data["requirements"]  # Dictionary: {"pick": 2, "ttb": 1}

    # Fetch associates from MongoDB based on login IDs
    associates = list(associates_collection.find({"login_id": {"$in": logins}}, {"_id": 0}))

    # Initialize assignments and unassigned logins
    assignments = {path: [] for path in requirements}
    unassigned = set(logins)  # Track unassigned logins

    # Assign associates based on permissions and availability
    for path, num_needed in requirements.items():
        # Convert path to lowercase for case-insensitive matching
        lowercase_path = path.lower()

        # Filter associates with the required permission (case-insensitive)
        eligible_associates = [a for a in associates if lowercase_path in [p.lower() for p in a.get("permissions", [])]]

        # Assign as many as needed
        assigned_logins = [a["login_id"] for a in eligible_associates[:num_needed]]
        assignments[path] = assigned_logins

        # Remove assigned logins from unassigned set
        unassigned -= set(assigned_logins)

    return jsonify({
        "assignments": assignments,
        "unassigned": list(unassigned)
    }), 200


# 📌 Temporary changes endpoints
@associates_bp.route("/temp-changes", methods=["POST"])
def create_temp_change_request():
    """Create a temporary add/remove request"""
    data = request.get_json()
    required_fields = ["change_type", "login_id", "requested_by"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if data["change_type"] not in ["add", "remove"]:
        return jsonify({"error": "Invalid change_type. Use 'add' or 'remove'"}), 400

    if data["change_type"] == "add" and not data.get("permissions"):
        return jsonify({"error": "Permissions required for add requests"}), 400

    temp_change = {
        "change_type": data["change_type"],
        "login_id": data["login_id"],
        "requested_by": data["requested_by"],
        "status": "pending",
        "expires_at": datetime.utcnow() + timedelta(hours=72)
    }

    if data["change_type"] == "add":
        temp_change.update({
            "name": data.get("name", ""),
            "permissions": data.get("permissions", [])
        })

    result = temp_changes_collection.insert_one(temp_change)
    return jsonify({
        "message": "Temporary change request created",
        "change_id": str(result.inserted_id)
    }), 201


@associates_bp.route("/temp-changes/pending", methods=["GET"])
def get_pending_temp_changes():
    """Get all pending temporary changes"""
    pending_changes = list(temp_changes_collection.find({"status": "pending"}))
    formatted_changes = []

    for change in pending_changes:
        formatted = {
            "id": str(change["_id"]),
            "change_type": change["change_type"],
            "login_id": change["login_id"],
            "requested_by": change["requested_by"],
            "expires_at": change["expires_at"].isoformat(),
        }
        if "name" in change:
            formatted["name"] = change["name"]
        if "permissions" in change:
            formatted["permissions"] = change["permissions"]
        formatted_changes.append(formatted)

    return jsonify(formatted_changes), 200


@associates_bp.route("/temp-changes/<string:change_id>/approve", methods=["POST"])
def approve_temp_change_request(change_id):
    """Approve a temporary change request"""
    try:
        obj_id = ObjectId(change_id)
    except:
        return jsonify({"error": "Invalid change ID format"}), 400

    change = temp_changes_collection.find_one({"_id": obj_id, "status": "pending"})
    if not change:
        return jsonify({"error": "Pending change not found"}), 404

    try:
        if change["change_type"] == "add":
            if associates_collection.find_one({"login_id": change["login_id"]}):
                return jsonify({"error": "Associate already exists"}), 409
            associates_collection.insert_one({
                "login_id": change["login_id"],
                "name": change.get("name", ""),
                "permissions": change.get("permissions", [])
            })
        else:
            result = associates_collection.delete_one({"login_id": change["login_id"]})
            if result.deleted_count == 0:
                return jsonify({"error": "Associate not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    temp_changes_collection.delete_one({"_id": obj_id})
    return jsonify({"message": "Change approved and applied successfully"}), 200


@associates_bp.route("/temp-changes/<string:change_id>/reject", methods=["POST"])
def reject_temp_change_request(change_id):
    """Reject a temporary change request"""
    try:
        obj_id = ObjectId(change_id)
    except:
        return jsonify({"error": "Invalid change ID format"}), 400

    result = temp_changes_collection.delete_one({"_id": obj_id, "status": "pending"})
    if result.deleted_count == 0:
        return jsonify({"error": "Pending change not found"}), 404

    return jsonify({"message": "Change rejected successfully"}), 200

