from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Category, Base, Item

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# first category
category1 = Category(name="Comedy")

session.add(category1)
session.commit()

item1 = Item(title="The Hangover", description="Three buddies wake up \
        from a bachelor party in Las Vegas, with no memory of the previous \
        night and the bachelor missing. They make their way around the city \
        in order to find their friend before wedding.", category=category1)

session.add(item1)
session.commit()

item2 = Item(title="Zootopia", description="The modern mammal metropolis of\
        Zootopia is a city like no other. Comprised of habitat neighborhoods \
        like ritzy Sahara Square and frigid Tundratown, it's a melting pot \
        where animals from every environment live together-a place where no \
        matter what you are, from the biggest elephant to the smallest shrew, \
        you can be anything.", category=category1)

session.add(item2)
session.commit()

# second category
category2 = Category(name="Romance")

session.add(category2)
session.commit()

item1 = Item(title="Casablanca", description="One of the most beloved \
        American films, this captivating wartime adventure of romance and \
        intrigue from director Michael Curtiz defies standard categorization. \
        Simply put, it is the story of Rick Blaine (Humphrey Bogart), a \
        world-weary ex-freedom fighter who runs a nightclub in Casablanca \
        during the early part of WWII. ", category=category2)

session.add(item1)
session.commit()

item2 = Item(title="The Philadelphia Story", description="Set among the \
        upper class in 1930s Philadelphia, this irreverent classic romantic \
        comedy features radiant performances by three legendary stars. On \
        the eve of her marriage to an uninteresting man, a headstrong \
        socialite jousts verbally with her charming ex-husband, drinks too \
        much champagne, and flirts outrageously with a handsome \
        reporter.", category=category2)

session.add(item2)
session.commit()

# third category
category3 = Category(name="Action & Adventure")

session.add(category3)
session.commit()

item1 = Item(title="Mad Max: Fury Road", description="Filmmaker George \
        Miller gears up for another post-apocalyptic action adventure with \
        Fury Road, the fourth outing in the Mad Max film series. Charlize \
        Theron stars alongside Tom Hardy (Bronson), with Zoe Kravitz, \
        Adelaide Clemens, and Rosie Huntington Whiteley heading up the \
        supporting cast. ~ Jeremy Wheeler, Rovi", category=category3)

session.add(item1)
session.commit()

item2 = Item(title="Wonder Woman", description="An Amazon princess \
        (Gal Gadot) finds her idyllic life on an island occupied only by \
        female warriors interrupted when a pilot (Chris Pine) crash-lands \
        nearby. After rescuing him, she learns that World War I is \
        engulfing the planet, and vows to use her superpowers to restore \
        peace. Directed by Patty Jenkins (Monster).", category=category3)

session.add(item2)
session.commit()

print "added category items!"
