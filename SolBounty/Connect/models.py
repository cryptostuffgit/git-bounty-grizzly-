from django.db import models
import uuid
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import jsonfield

# Create your models here.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

class GitRepository(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	github_id = models.IntegerField(null=True, blank=True)
	name = models.CharField(max_length=256,null=True, blank=True)

	def __str__(self):
		return self.user.username + "/" + self.name

class GitIssue(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	repository = models.ForeignKey(GitRepository, on_delete=models.CASCADE)
	github_id = models.IntegerField(null=True, blank=True)
	title = models.CharField(max_length=256,null=True, blank=True)
	body = models.TextField(null=True, blank=True)
	lamports = models.IntegerField(null=True, blank=True)
	minimum_date = models.DateTimeField(null=True, blank=True)
	is_active = models.BooleanField(default=True)
	pda = models.CharField(max_length=256,null=True, blank=True)
	branch_name = models.CharField(max_length=256,null=True, blank=True)
	
	@property
	def pda_link(self):
		return f'https://explorer.solana.com/address/{self.pda}?cluster=devnet'
	
	def __str__(self):
		return self.repository.name + " | " + str(self.github_id)


class BountyHunter(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	issue = models.ForeignKey(GitIssue, on_delete=models.CASCADE)
	wallet = models.CharField(max_length=256,null=True, blank=True)


class GitWebhook(models.Model):
	data = jsonfield.JSONField(null=True, blank=True) 
	timestamp = models.DateTimeField(auto_now_add=True,null=True, blank=True)


class BountyPayment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	issue = models.ForeignKey(GitIssue, on_delete=models.CASCADE)