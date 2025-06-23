import os
from datetime import datetime, date, timedelta
import random
from faker import Faker

# Load environment variables from .env if not already loaded
from dotenv import load_dotenv
load_dotenv()

# Import db, app, and bcrypt from config.py
# Import all models
from config import app, db, bcrypt
from models.user import User
from models.guest import Guest
from models.episode import Episode
from models.appearance import Appearance

# Initialize Faker
fake = Faker()

# Define a function to clean and seed the database
def seed_database():
    with app.app_context(): # Ensure we are within the Flask application context
        print("Clearing old data...")
        # Delete data from tables in reverse order of dependency
        Appearance.query.delete()
        Guest.query.delete()
        Episode.query.delete()
        User.query.delete()
        db.session.commit()
        print("Old data cleared.")

        print("Seeding users...")
        users = []
        # Create a few demo users
        user1 = User(username='testuser')
        user1.password_hash = 'password123' # This will be hashed by the setter
        users.append(user1)

        user2 = User(username='admin')
        user2.password_hash = 'adminpass'
        users.append(user2)

        user3 = User(username='guestuser')
        user3.password_hash = 'guestpass'
        users.append(user3)
        
        db.session.add_all(users)
        db.session.commit()
        print(f"Seeded {len(users)} users.")

        print("Seeding guests...")
        guests = []
        for _ in range(20): # Create 20 random guests
            guest = Guest(
                name=fake.name(),
                occupation=fake.job()
            )
            guests.append(guest)
        db.session.add_all(guests)
        db.session.commit()
        print(f"Seeded {len(guests)} guests.")

        print("Seeding episodes...")
        episodes = []
        start_date = datetime.now() - timedelta(days=365) # Start from a year ago
        for i in range(50): # Create 50 episodes
            episode = Episode(
                date=(start_date + timedelta(days=i*7)).date(), # One episode per week
                number=i + 1 # Simple ascending number
            )
            episodes.append(episode)
        db.session.add_all(episodes)
        db.session.commit()
        print(f"Seeded {len(episodes)} episodes.")

        print("Seeding appearances...")
        appearances = []
        # Create random appearances linking guests and episodes
        for _ in range(100): # Create 100 appearances
            random_guest = random.choice(guests)
            random_episode = random.choice(episodes)
            
            # Ensure unique guest-episode pair for appearances if desired, or allow multiple
            # unless a unique constraint is added in the model.
            appearance = Appearance(
                rating=random.randint(1, 5), # Rating between 1 and 5
                guest=random_guest,
                episode=random_episode
            )
            appearances.append(appearance)
        
        db.session.add_all(appearances)
        db.session.commit()
        print(f"Seeded {len(appearances)} appearances.")

        print("Database seeding complete!")

if __name__ == '__main__':
    seed_database()
