def get_student_by_name(client, name):
    return client['fyp']['student'].find_one({'name': name})

def create_student(client, name, age):
    return client['fyp']['student'].insert_one({"name": name, "age": age})




    #detele

   # update