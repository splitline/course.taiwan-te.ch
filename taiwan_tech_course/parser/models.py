from django.db import models

class Courses(models.Model):
    class Meta:
        unique_together = (('semester', 'course_id'),)
    id = models.CharField(primary_key=True, default=None, max_length=15)
    semester = models.CharField(max_length=10)
    course_id = models.CharField(max_length=10)
    ge_type = models.CharField(max_length=1)
    name = models.CharField(max_length=50)
    outline_link = models.CharField(max_length=128)
    credit = models.IntegerField()
    required_subject = models.BooleanField()
    lecturer = models.CharField(max_length=50)
    classroom = models.CharField(max_length=50)
    periods = models.CharField(max_length=1024)
    # detail_link = models.CharField(max_length=128)
    note = models.TextField()

    def id_gen(self):
        return self.semester + "-" + self.course_id

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.id_gen()
        super(Courses, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.semester + "-" + self.course_id + " " + self.name)
