from pymongo import MongoClient

def database():
  client = MongoClient("mongodb+srv://GavinduTharaka:Gavindu123@sinhalasubdownbot.1v9ix.mongodb.net/Bot?retryWrites"
                       "=true&w=majority")
  db = client["Bot"]
  users = db['All_users']
  counts = db['counts']


  def update_users(details):
      _id = details["_id"]
      try:
          username = details["username"]
          users.update_one({'_id': _id}, {"$set": {"username": "@" + str(username)}} )
          print("updated username")
      except Exception as e:
          print("Not UserName ", e)
          pass

      try:
          status = str(details['status'])
          print(status)
          users.update_one({'_id': _id},  {"$set": {'status' : status}})
          print("updated status")
      except Exception as e:
          print("Not Status ",e)
          pass


  def insert_users(details):
      try:
          _id = details["_id"]
          username = details["username"]
          status = "active"
          users.insert_one({"_id": _id, "username": "@"+str(username), 'status': status})
      except:
          update_users(details)
          pass


  def count_users():
      try:
          count = db.All_users.estimated_document_count()
          print(count)
          return count
      except Exception as e:
          print(e)
          pass


  def delete_users():
      try:
          count = db.All_users.find({'status': 'delete'})
          return count
      except Exception as e:
          print(e)
          pass


  def all_users():
      try:
          data = db.All_users.find()
          _id = []
          status = []
          username = []
          for i in data:
              _id.append(i["_id"])
              username.append(i["username"])
              status.append(i["status"])
          output = {"_id": _id, "username": username, "status": status}
          return output

      except:
          pass


  def delete_user_count():
      count = 0
      for i in delete_users():
          count = count + 1
      return count


  def active_user_count():
      try:
          data = db.All_users.find({'status': 'active'})
          count = 0
          for i in data:
              count = count + 1
          print()
          return count
      except Exception as e:
          print(e)
          pass
