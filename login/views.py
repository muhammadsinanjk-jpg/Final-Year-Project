
from django.shortcuts import render
from .models import Login
from django.http import HttpResponseRedirect
from register_for_buyer.models import RegisterForBuyer
from register_for_seller.models import RegisterForSeller

from django.shortcuts import render
from django.http import HttpResponseRedirect

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use filter instead of get to handle case-insensitive DB collation & multiple matches
        logins = Login.objects.filter(username=username)

        # Perform exact case-sensitive password check
        ob = None
        for l in logins:
            if l.password == password:
                ob = l
                break

        if not ob:
            ob = logins.filter(password=password).first()

        if not ob:
            return render(request, 'login/login.html', {
                'msg': 'Username or password is incorrect'
            })

        tp = ob.type
        uid = ob.u_id

        # ADMIN
        if tp == 'admin':
            request.session['u_id'] = uid
            return HttpResponseRedirect('/temp/admin/')

        # BUYER
        elif tp == 'buyer':
            request.session['u_id'] = uid
            return HttpResponseRedirect('/temp/buyer/')


        # SELLER
        elif tp == 'seller':
            try:
                seller = RegisterForSeller.objects.get(sreg_id=uid)

                if seller.status == 'accepted':
                    request.session['u_id'] = uid
                    return HttpResponseRedirect('/temp/seller/')

                elif seller.status == 'pending':
                    msg = 'Your seller account is pending approval.'

                elif seller.status == 'rejected':
                    msg = 'Your seller account has been rejected.'

                else:
                    msg = 'Invalid seller status.'

            except RegisterForSeller.DoesNotExist:
                msg = 'Seller account not found.'

        return render(request, 'login/login.html', {'msg': msg})

    return render(request, 'login/login.html')

def forgotpassword(request):
    if request.method == 'POST':
        em = request.POST.get('email')
        import smtplib

        # check seller
        seller = RegisterForSeller.objects.filter(email=em).first()

        if seller:
            email = "projectmailbg@gmail.com"
            sub = "Password Recovery"
            msg = seller.password

        else:
            # check buyer
            buyer = RegisterForBuyer.objects.filter(email=em).first()
            if buyer:
                email = "projectmailbg@gmail.com"
                sub = "Password Recovery"
                msg = buyer.password
            else:
                return render(request, 'login/forgott.html', {
                    'error': 'Email not registered'
                })

        text = f"Subject: {sub}\n\n{msg}"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, "iqjjrhsyerovorav")
        server.sendmail(email, em, text)
        server.quit()

        return render(request, 'login/forgott.html', {
            'success': 'Password sent to your email'
        })

    return render(request, 'login/forgott.html')

def logout(request):
    request.session.clear()
    return HttpResponseRedirect('/login/log/')