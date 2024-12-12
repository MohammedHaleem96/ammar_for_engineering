from app import db
from werkzeug.security import generate_password_hash
from app.models.admins import Admin

# Create a test user
test_user = Admin(username="testuser")
test_user.set_password("testpassword")

# Add the test user to the database
db.session.add(test_user)
db.session.commit()

print("Test user added!")