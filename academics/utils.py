def is_admin(user):
    return user.profile.role == 'admin'

def is_teacher(user):
    return user.profile.role == 'teacher'

def is_student(user):
    return user.profile.role == 'student'