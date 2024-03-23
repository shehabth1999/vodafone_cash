from django.db import models

class TeachersHasStudents(models.Model):
    teachers_idsubjects = models.IntegerField(db_column='teachers_idSubjects', primary_key=True)  
    students_idsubjects = models.ForeignKey(Students, models.DO_NOTHING, db_column='students_idSubjects')  

    class Meta:
        managed = False
        db_table = 'teachers_has_students'
        unique_together = (('teachers_idsubjects', 'students_idsubjects'),)


class TeachersHasSubjects(models.Model):
    teachers_id = models.IntegerField(primary_key=True)
    teachers_users_idsubjects = models.IntegerField(db_column='teachers_users_idSubjects')  
    subjects = models.ForeignKey(Subjects, models.DO_NOTHING, db_column='Subjects_id')  

    class Meta:
        managed = False
        db_table = 'teachers_has_subjects'
        unique_together = (('teachers_id', 'teachers_users_idsubjects', 'subjects'),)


class StudentsHasEscort(models.Model):
    students = models.OneToOneField(Students, models.DO_NOTHING, primary_key=True)
    students_users_idsubjects = models.ForeignKey(Students, models.DO_NOTHING, db_column='students_users_idSubjects', to_field='users_idSubjects')  
    escort = models.ForeignKey(Escort, models.DO_NOTHING)
    escort_users = models.ForeignKey(Escort, models.DO_NOTHING, to_field='users_id')

    class Meta:
        managed = False
        db_table = 'students_has_escort'
        unique_together = (('students', 'students_users_idsubjects', 'escort', 'escort_users'),)


class StudentsHasSubjects(models.Model):
    students_id = models.IntegerField(primary_key=True)
    students_users_idsubjects = models.IntegerField(db_column='students_users_idSubjects')  
    subjects = models.ForeignKey('Subjects', models.DO_NOTHING, db_column='Subjects_id')  

    class Meta:
        managed = False
        db_table = 'students_has_subjects'
        unique_together = (('students_id', 'students_users_idsubjects', 'subjects'),)

