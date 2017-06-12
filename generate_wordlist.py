import csv
import codenames.models as models
from codenames import db


db.create_all()

with open('wordlist.csv', 'r') as f:
	reader = csv.reader(f)
	for row in reader:
		word = models.Word('.'.join(row))
		db.session.add(word)
	db.session.commit()