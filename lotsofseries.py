# A python code for adding several series with episodes to "series.db"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Series, Base, Episode, User
# coding=utf-8
engine = create_engine('sqlite:///series.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Mr. Popo", email="popo@kamehameha.com",
             picture='https://i.ytimg.com/vi/fXlO7Rd3oHA/maxresdefault.jpg')
session.add(User1)
session.commit()

# Adding TV Series Sherlock
sherlock = Series(user_id=1, name="Sherlock", rating=9.2, actors="""Benedict
 Cummberbatch & Martin Freeman""")
session.add(sherlock)
session.commit()

# Adding episodes of Sherlock
episode1 = Episode(user_id=1, name="Unaired Pilot", description="""Invalided
 home from the war in Afghanistan, Dr. John Watson becomes roommates with
 the world's only "consulting detective," Sherlock Holmes. Within a day their
 friendship is forged and
 several murders are solved. """, air_date="05 Jun. 2011", series=sherlock)
session.add(episode1)
session.commit()

episode2 = Episode(user_id=1, name="A Study in Pink", description="""War vet
 Dr. John Watson returns to London in need of a place to stay. He meets
 Sherlock Holmes, a consulting detective, and the two soon find themselves
 digging into a
 string of serial "suicides." """, air_date="24 Oct. 2010", series=sherlock)
session.add(episode2)
session.commit()

episode3 = Episode(user_id=1, name="The Blind Banker", description="""
Mysterious symbols and murders are showing up all over London, leading
 Sherlock and John to a secret Chinese crime syndicate called Black
 Lotus. """, air_date="31 Oct. 2010", series=sherlock)
session.add(episode3)
session.commit()

episode4 = Episode(user_id=1, name="The Great Game", description="""Mycroft
 needs Sherlock's help, but a remorseless criminal mastermind puts Sherlock
 on a distracting crime-solving spree via a series of hostage human bombs
 through which he speaks. """, air_date="7 Nov. 2010", series=sherlock)
session.add(episode4)
session.commit()

episode5 = Episode(user_id=1, name="A Scandal in Belgravia", description="""
Sherlock must confiscate something of importance from a mysterious woman named
 Irene Adler. """, air_date="6 May 2012", series=sherlock)
session.add(episode5)
session.commit()

episode6 = Episode(user_id=1, name="The Hounds of Baskerville", description="""
Sherlock and John investigate the ghosts of a young man who has been seeing
 monstrous hounds out in the woods where his father
 died. """, air_date="13 May 2012", series=sherlock)
session.add(episode6)
session.commit()

episode7 = Episode(user_id=1, name="The Reichenbach Fall", description="""Jim
 Moriarty hatches a mad scheme to turn the whole city against
 Sherlock. """, air_date="20 May 2012", series=sherlock)
session.add(episode7)
session.commit()


# # Adding TV Series Friends
friends = Series(user_id=1, name="F.R.I.E.N.D.S.", rating=9.0, actors="""
Jennifer Aniston, Courteney Cox, Lisa Kudrow, Matthew Perry, Matt Leblanc""")
session.add(friends)
session.commit()

# Adding episodes of Friends
episode8 = Episode(user_id=1, name="""The One Where Monica Gets
 a Roommate""", description="""Monica and the gang introduce Rachel to the
 "real world" after she leaves her fiance
 at the altar """, air_date="22 Sep. 1994 ", series=friends)
session.add(episode8)
session.commit()

episode9 = Episode(user_id=1, name="""The One with the Sonogram at the
 End""", description="""Ross finds out his ex-wife is pregnant. Rachel returns
 her engagement ring to Barry. Monica becomes stressed when her and Ross's
 parents come to visit.""", air_date="29 Sep. 1994", series=friends)
session.add(episode9)
session.commit()

episode10 = Episode(user_id=1, name="The One with the Thumb", description="""
Monica becomes irritated when everyone likes her new boyfriend more than she
 does. Chandler resumes his smoking habit. Phoebe is given $7000 when she finds
 a thumb in a can of soda """, air_date="6 Oct. 1994 ", series=friends)
session.add(episode10)
session.commit()

episode11 = Episode(user_id=1, name="""The One with George
 Stephanopoulos""", description="""Joey and Chandler take Ross to a hockey game
 to take his mind off the anniversary of the first time he slept with Carol,
 while the girls become depressed when they realize they don't have a
 'plan'. """, air_date="13 Oct. 1994", series=friends)
session.add(episode11)
session.commit()

episode12 = Episode(user_id=1, name="""The One with the East German Laundry
 Detergent""", description="""Eager to spend time with Rachel, Ross pretends
 his washroom is rat-infested so he can join her at the laundromat. Meanwhile,
 Joey has Monica pose as his girlfriend, and Chandler struggles to break up
 with his girlfriend """, air_date="20 Oct. 1994", series=friends)
session.add(episode12)
session.commit()

episode13 = Episode(user_id=1, name="The One with the Butt", description="""
Monica's obsessiveness is put to the test after Rachel cleans the apartment.
 Joey lands a film role as Al Pacino's butt double. Chandler enjoys a
 relationship with all of the fun but none of the
 responsibility.""", air_date="27 Oct. 1994", series=friends)
session.add(episode13)
session.commit()

episode14 = Episode(user_id=1, name="The One with the Blackout", description="""
When New York suffers from a blackout, Ross tries to tell Rachel that he likes
 her, and Chandler gets stuck in an ATM vestibule with a
 model.""", air_date="3 Nov. 1994", series=friends)
session.add(episode14)
session.commit()


# # Adding TV Series Breaking Bad
breaking_bad = Series(user_id=1, name="Breaking Bad", rating=9.5, actors="""
Bryan Cranston & Aaron Paul""")
session.add(breaking_bad)
session.commit()

# Adding episodes of Breaking Bad
episode15 = Episode(user_id=1, name="Pilot", description="""
Diagnosed with terminal lung cancer, chemistry teacher Walter White teams
 up with his former student, Jesse Pinkman, to cook and sell crystal
 meth.""", air_date="20 Jan. 2008", series=breaking_bad)
session.add(episode15)
session.commit()

episode16 = Episode(user_id=1, name="Cat's in the Bag...", description="""
After their first drug deal goes terribly wrong, Walt and Jesse are forced to
 deal with a corpse and a prisoner. Meanwhile, Skyler grows suspicious of
 Walt's activities. """, air_date="27 Jan. 2008 ", series=breaking_bad)
session.add(episode16)
session.commit()

episode17 = Episode(user_id=1, name="""...And the Bag's in the River
""", description="""Walt is struggling to decide if it's best to kill Krazy 8
 or let him go. """, air_date="10 Feb. 2008 ", series=breaking_bad)
session.add(episode17)
session.commit()

episode18 = Episode(user_id=1, name="Cancer Man", description="""Walt tells the
 rest of his family about his cancer. Jesse tries to make amends with his own
 parents. """, air_date="17 Feb. 2008 ", series=breaking_bad)
session.add(episode18)
session.commit()

episode19 = Episode(user_id=1, name="Gray Matter", description="""Walt rejects
 everyone who tries to help him with the cancer. Jesse tries his best to create
 Walt's meth, with the help of an old
 friend. """, air_date="24 Feb. 2008 ", series=breaking_bad)
session.add(episode19)
session.commit()

episode20 = Episode(user_id=1, name="Crazy Handful of Nothin'", description="""
With the side effects and cost of his treatment mounting, Walt demands that
 Jesse finds a wholesaler to buy their drugs, which lands him in
 trouble. """, air_date="2 Mar. 2008 ", series=breaking_bad)
session.add(episode20)
session.commit()


# # Adding TV Series Mr. Robot
robot = Series(user_id=1, name="Mr. Robot", rating=8.7, actors="""
Rami Malek, Christian Slater, Portia Doubleday""")
session.add(robot)
session.commit()

# Adding episodes of Mr. Robot
episode21 = Episode(user_id=1, name="hellofriend", description="""A notorious
 hacker takes an interest in cyber security engineer and vigilante styled
 computer hacker Elliot, while an evil corporation is
 hacked.""", air_date="24 Jun. 2015", series=robot)
session.add(episode21)
session.commit()

episode22 = Episode(user_id=1, name="ones-and-zer0es", description="""Elliot is
 torn between accepting a lucrative yet problematic job offer and joining the
 fsociety hacker group. """, air_date="1 Jul. 2015 ", series=robot)
session.add(episode22)
session.commit()

episode23 = Episode(user_id=1, name="d3bug", description="""Elliot attempts to
 lead a normal life, but cannot escape fsociety, while Gideon grows suspicious,
 and Tyrell plays dirty. """, air_date="8 Jul. 2015 ", series=robot)
session.add(episode23)
session.commit()

episode24 = Episode(user_id=1, name="da3m0ns", description="""While dealing
 with his withdrawal, Elliot suffers a series of hallucinations about his life,
 while Shayla helps Angela take an unexpected trip.
 """, air_date="15 Jul. 2015 ", series=robot)
session.add(episode24)
session.commit()

episode25 = Episode(user_id=1, name="3xpl0its", description="""Fsociety
 attempts to penetrate Steel Mountain, the most secure data facility in
 America, while Angela makes an important decision.
 """, air_date="22 Jul. 2015 ", series=robot)
session.add(episode25)
session.commit()

# Adding TV Series Game Of Thrones
got = Series(user_id=1, name="Game of Thrones", rating=9.5, actors="""
Emilia Clarke, Peter Dinklage, Kit Harington""")
session.add(got)
session.commit()

# Adding episodes Game of Thrones
episode26 = Episode(user_id=1, name="Winter Is Coming", description="""Jon
 Arryn, the Hand of the King, is dead. King Robert Baratheon plans to ask his
 oldest friend, Eddard Stark, to take Jon's place. Across the sea, Viserys
 Targaryen plans to wed his sister to a nomadic warlord in exchange for an
 army. """, air_date="17 Apr. 2011 ", series=got)
session.add(episode26)
session.commit()

episode27 = Episode(user_id=1, name="The Kingsroad", description="""While
 Bran recovers from his fall, Ned takes only his daughters to Kings Landing.
 Jon Snow goes with his uncle Benjen to The Wall. Tyrion joins them.
 """, air_date="24 Apr. 2011 ", series=got)
session.add(episode27)
session.commit()

episode28 = Episode(user_id=1, name="Lord Snow", description="""Lord Stark and
 his daughters arrive at King's Landing to discover the intrigues of the
 king's realm.""", air_date="1 May 2011 ", series=got)
session.add(episode28)
session.commit()

episode29 = Episode(user_id=1, name="""
Cripples, Bastards, and Broken Things""", description="""Eddard investigates
 Jon Arryn's murder. Jon befriends Samwell Tarly, a coward who has come to join
 the Night's Watch.""", air_date="8 May 2011 ", series=got)
session.add(episode29)
session.commit()

episode30 = Episode(user_id=1, name="The Wolf and the Lion", description="""
Catelyn has captured Tyrion and plans to bring him to her sister, Lysa Arryn,
 at The Vale, to be tried for his, supposed, crimes against Bran. Robert plans
 to have Daenerys killed, but Eddard refuses to be a part of it and quits.
 """, air_date="15 May 2011 ", series=got)
session.add(episode30)
session.commit()


# # # Adding TV Series
# a=Series(user_id=1, name="", rating=9.0, actors="" )
# session.add(a)
# session.commit()

# episode = Episode(user_id=1, name="",
#  description=""" """,
#  air_date="", series=)
# session.add(episode)
# session.commit()

print "added new episodes!"
