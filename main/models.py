from django.db import models

class people_data(models.Model):
	username = models.CharField(max_length=30)
	name = models.CharField(max_length=30)
	email = models.CharField(max_length=30)
	phone = models.CharField(max_length=13)
	password = models.CharField(max_length=30)
	course=models.CharField(max_length=4)
	gender=models.CharField(max_length=10)
	address=models.CharField(max_length=100)
	profile_img = models.ImageField(upload_to='images/')
	date_joined = models.DateTimeField()
	last_login = models.DateTimeField()
	status=models.CharField(max_length=20)
	reg_type=models.CharField(max_length=30)
	email_key=models.CharField(max_length=10)
	birth=models.DateField()

	def __str__(self):
		return self.username
class people_post(models.Model):
	post_data=models.CharField(max_length=400)
	username=models.CharField(max_length=30)
	post_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.username
class frendship(models.Model):
	user_one_id=models.IntegerField()
	user_two_id=models.IntegerField()
	status=models.IntegerField()
	action_user_id=models.IntegerField()
	def __str__(self):
		return self.action_user_id
# Create your models here.
