from django.db import models
from django.contrib.auth.models import User

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    account_number = models.IntegerField()
    easy_saver_balance = models.FloatField(default=0)
    loan_balance = models.FloatField(default=0)
    total_balance = models.FloatField(default=0)
    profile_image = models.ImageField(upload_to="profile_images")

    def __str__(self):
        return self.user.username

TransactionChoices = (
    ('Deposit', 'deposit'),
    ('Withdrawal', 'withdrawal'),
    ('Savings', 'savings'),
    ('Transfer', 'transfer')
)

StatusChoices = (
    ('Pending', 'pending'),
    ('Confirmed', 'confirmed'),
    ('Declined', 'Declined')
)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    trans_type = models.CharField(choices=TransactionChoices, max_length=30)
    status = models.CharField(max_length=10, choices=StatusChoices)
    amount = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return self.user.username
