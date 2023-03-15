from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(GitRepository)
admin.site.register(GitIssue)
admin.site.register(GitWebhook)
admin.site.register(BountyPayment)