import crud
import model
import server

os.system('dropdb habits')
os.system('createdb habits')
model.connect_to_db(server.app)
model.db.create_all()