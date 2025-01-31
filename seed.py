# Standard library imports
from random import randint, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, Community, User, Event, Estate, Notification

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")

       
        db.session.query(Community).delete()
        db.session.query(User).delete()
        db.session.query(Event).delete()
        db.session.query(Estate).delete()
        db.session.query(Notification).delete()
        db.session.commit()

     
        communities = []
        for _ in range(5): 
            community = Community(
                name=fake.city(),
                location=fake.street_address()
            )
            communities.append(community)
            db.session.add(community)

        # Create Users
        users = []
        for _ in range(7):  # Creating 20 users
            community = rc(communities)
            user = User(
                name=fake.name(),
                email=fake.email(),
                occupation=fake.job(),
                phoneno=fake.pyint(min_value=1000000000, max_value=9999999999),  # Assumes 10 digit phone number
                houseno=fake.pyint(min_value=1, max_value=1000),
                community=community
            )
            users.append(user)
            db.session.add(user)

        # Create Events
        for _ in range(10):  # Creating 10 events
            community = rc(communities)
            event = Event(
                eventname=fake.sentence(nb_words=3, variable_nb_words=True),
                eventdate=fake.future_datetime(end_date="+30d"),
                community=community
            )
            db.session.add(event)

        
        for _ in range(15): 
            community = rc(communities)
            user = rc(users)
            estate = Estate(
                estatename=fake.street_name(),
                user=user,
                community=community
            )
            db.session.add(estate)

       
        for _ in range(30):  
            user = rc(users)
            community = rc(communities)
            notification = Notification(
                name=fake.sentence(nb_words=6),
                rsvp=rc(['yes', 'no', 'maybe']),  
                user=user,
                community=community
            )
            db.session.add(notification)

        db.session.commit()
        print("Seeding complete!")