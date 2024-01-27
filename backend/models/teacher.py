def get_teacher_by_name(client, name):
    return client['fyp']['teacher'].find_one({'name': name})