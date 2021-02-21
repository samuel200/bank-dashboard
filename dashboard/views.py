from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

from .models import UserDetail, Transaction

from datetime import datetime

@login_required(login_url="auth:login")
def index_view(request):
    transactions = Transaction.objects.filter(user=request.user, status='confirmed')
    if not request.user.is_staff:
        detail = UserDetail.objects.get(user=request.user)
        loan_balance = "{0:,.2f}".format(detail.loan_balance)
        easy_saver_balance = "{0:,.2f}".format(detail.easy_saver_balance)
        total_balance = "{0:,.2f}".format(detail.total_balance)
        available_balance = detail.total_balance - detail.easy_saver_balance
        context = {"loan_balance": loan_balance, "easy_saver_balance": easy_saver_balance, "total_balance": total_balance, "available_balance": available_balance, "transactions": transactions, "details": detail}
        return render(request, 'dashboard/index.html', context=context)
    return redirect("auth:login")

@login_required(login_url="auth:login")
def transactions_view(request):
    detail = UserDetail.objects.get(user=request.user)
    return render(request, 'dashboard/transactions.html', {"details": detail})

@login_required(login_url="auth:login")
def savings_view(request):
    detail = UserDetail.objects.get(user=request.user)
    loan_balance = "{0:,.2f}".format(detail.loan_balance)
    easy_saver_balance = "{0:,.2f}".format(detail.easy_saver_balance)
    total_balance = "{0:,.2f}".format(detail.total_balance)
    available_balance = detail.total_balance - detail.easy_saver_balance

    saving_transactions = Transaction.objects.filter(user=request.user, trans_type="savings", status="confirmed")
    context = {"saving_transactions": saving_transactions, "transaction_count": len(saving_transactions), "loan_balance": loan_balance, "easy_saver_balance": easy_saver_balance, "total_balance": total_balance, "available_balance": available_balance, "details": detail}
    return render(request, 'dashboard/savings.html', context=context)

@login_required(login_url="auth:login")
def send_funds_view(request):
    if request.method.lower() == "post":
        name = request.POST['name'] 
        account_number = request.POST['account-number'] 
        financial_institution = request.POST['financial-institution'] 
        amount = request.POST['amount']
        detail = UserDetail.objects.get(user=request.user)
        loan_balance = "{0:,.2f}".format(detail.loan_balance)
        easy_saver_balance = "{0:,.2f}".format(detail.easy_saver_balance)
        total_balance = "{0:,.2f}".format(detail.total_balance)
        available_balance = detail.total_balance - detail.easy_saver_balance

        if float(amount) < 10:
            return render(request, 'dashboard/send-funds.html', {
                "error_message": "Amount provided is less than minimum transaction amount of $10".capitalize(),
                "name": name,
                "account_number": account_number,
                "financial_institution": financial_institution,
                "details": detail
            })
        elif float(amount) > available_balance:
            return render(request, 'dashboard/send-funds.html', {
                "error_message": "Amount provided is more than your available account balance".capitalize(),
                "name": name,
                "account_number": account_number,
                "financial_institution": financial_institution,
                "details": detail
            })
        else:
            transactions = Transaction.objects.create(user=request.user, trans_type="transfer", amount=float(amount), date=datetime.now(), status="confirmed")
            money_difference = detail.total_balance - detail.easy_saver_balance

            # if money_difference - float(amount) > 0:
            #     detail.total_balance -= float(amount)
            # else:
            #     detail.easy_saver_balance += (money_difference - amount)
            #     detail.total_balance = detail.easy_saver_balance

            detail.total_balance -= float(amount)
            detail.save()
            return render(request, 'dashboard/send-funds.html', {"success_message": "Transfer made successfully".capitalize(), "details": detail})
    else:
        if not request.user.is_staff:
            detail = UserDetail.objects.get(user=request.user)
            loan_balance = "{0:,.2f}".format(detail.loan_balance)
            easy_saver_balance = "{0:,.2f}".format(detail.easy_saver_balance)
            total_balance = "{0:,.2f}".format(detail.total_balance)
            available_balance = detail.total_balance - detail.easy_saver_balance
            context = {"loan_balance": loan_balance, "easy_saver_balance": easy_saver_balance, "total_balance": total_balance, "available_balance": available_balance, "details": detail}
            return render(request, 'dashboard/send-funds.html', context=context)
        return redirect("auth:login")

@login_required(login_url="auth:login")
def loans_view(request):
    detail = UserDetail.objects.get(user=request.user)
    if request.method.lower() == "post":
        return render(request, 'dashboard/loans.html', {"success_message": "Your Loan Request Has Been Made Successfully Await Our Respons Which Will Be Sent To Your Provided Email Address.", "details": detail})
    return render(request, 'dashboard/loans.html', {"details": detail})

@login_required(login_url="auth:login")
def customer_support_view(request):
    detail = UserDetail.objects.get(user=request.user)
    if request.method.lower() == 'post':
        d = { 'name': request.POST['full-name'], 'message': request.POST['message'] }
        subject, from_email, to = f"Customer Support Message From {request.POST['full-name']}", settings.EMAIL_HOST_USER, request.POST['email']
        text_content = get_template('email.txt')
        html_content = get_template('email.html')
        msg = EmailMultiAlternatives(subject, text_content.render(d), from_email, [to])
        msg.attach_alternative(html_content.render(d), "text/html")
        msg.send()
        return render(request, 'dashboard/customer-support.html', {"success_message": "Your message has been sent successfully".capitalize(), "details": detail})
    return render(request, 'dashboard/customer-support.html', {"details": detail})

def logout_view(request):
    logout(request)
    return redirect("auth:login")