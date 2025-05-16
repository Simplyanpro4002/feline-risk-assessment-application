from app import app, db
from models import User

def init_db():
    with app.app_context():
        # Create all database tables
        db.create_all()

        # Check if admin user already exists
        admin_user = User.query.filter_by(email='admin@example.com').first()
        if not admin_user:
            # Create admin user
            admin = User(
                email='admin@example.com',
                name='Admin User'
            )
            admin.set_password('Admin123!')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists!")

if __name__ == '__main__':
    init_db() 