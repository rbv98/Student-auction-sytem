from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Users, Auctions, Auctioneditems, Bids, Message
import datetime
from django.db import connection


def testmysql(request):
    user = Users.objects.all()
    context = {
    'userid': user[1].userid,
    'name': user[1].name,
    }
    return render(request, 'home.html', context)

def hero_page(request):
    # Add logic to fetch data for hero page
    return render(request, 'hero_page.html')

from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.type = 'Normal'  # Set default value for 'Type' field
            user.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_logout(request):
    request.session.flush()  # Clear all session data
    return redirect('hero_page')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Retrieve user based on email
        try:
            user = Users.objects.get(email=email)
        except Users.DoesNotExist:
            user = None
            return redirect('hero_page')
        
        if user is not None:
            if password == user.password:
                if user.type == 'Admin':
                    # Redirect admin user to admin page
                    return redirect('admin_page')
                else:
                    # Store user id in session
                    request.session['user_id'] = user.userid
                    # Redirect other users to auctions page or any other appropriate page
                    return redirect('auctions')
            else:
                error_message = 'Incorrect password'
        else:
            error_message = 'User does not exist'

        return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')




def admin_page(request):
    results = None
    error_message = None
    if request.method == 'POST':
        query = request.POST.get('query')
        try:
            # Execute the raw SQL query
            with connection.cursor() as cursor:
                cursor.execute(query)
                # Fetch all the rows from the cursor
                columns = [col[0] for col in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            error_message = str(e)
            print("Error executing query:", error_message)  
            return render(request, 'admin_page.html', {'error_message': error_message})
    return render(request, 'admin_page.html', {'results': results})




def landing_page(request):
    return render(request, 'landing_page.html')


def auctions(request):
    user_id = request.session.get('user_id')
    if(user_id is None):
        return redirect('login')
    auctions = Auctions.objects.all()

    # Pass the auctions queryset to the template for rendering
    return render(request, 'auctions.html', {'auctions': auctions})

def messages(request):
    user_id = request.session.get('user_id')
    if(user_id is None):
        return redirect('login')
    
    messages_sent = Message.objects.filter(senderid=user_id)
    messages_recd = Message.objects.filter(receiverid=user_id)
    users = []
    for message in messages_sent:
        users.append([message.receiverid.userid, message.receiverid.name])
        
    return render(request, 'messages.html', {'sent': messages_sent, 'recd': messages_recd, 'users': users})


def auction(request, auctionid):
    user_id = request.session.get('user_id')
    if(user_id is None):
        return redirect('hero_page')
    #auction_items = Auctioneditems.objects.filter(auctionid=auctionid)
    auction_items = Auctioneditems.objects.filter(auctionid=auctionid)
    
    item_list = []
    print(auction_items)
    # Loop through each auction item
    for item in auction_items:
        print(item.itemid)
        # Retrieve the product name associated with the current auction item
        product_name = item.productid.name
        # Append a sublist with the itemid and product name to the final list

        print(item)
        item_list.append([item.itemid, product_name])

    print(item_list)
    return render(request, 'auction.html', {'auctionid': auctionid, 'item_list': item_list})


def auctionitem(request, itemid):
    user_id = request.session.get('user_id')
    if(user_id is None):
        return redirect('hero_page')
    auctionitem = get_object_or_404(Auctioneditems, itemid=itemid)
    
    bids = Bids.objects.filter(itemid=itemid)
    return render(request, 'auctionitem.html', {'auctionitem': auctionitem, 'bids': bids})



def placebid(request):
    if request.method == 'POST':
        bid_amount = float(request.POST.get('bid_amount'))
        itemid = request.POST.get('itemid')  
        
        # Validate bid_amount if necessary
        bids = Bids.objects.filter(itemid=itemid)
        latest_bid = bids.order_by('-bidtimestamp').first()
        
        for bid in bids:
            print(bid.bidid, bid.amount, bid.bidtimestamp)

        if bid_amount > latest_bid.amount:
            
            auctionitem = get_object_or_404(Auctioneditems, itemid=itemid)
            
            user_id = request.session.get('user_id')
            if user_id:
                user = get_object_or_404(Users, userid=user_id)
                
                bid = Bids(amount=bid_amount, itemid=auctionitem, bidderid=user, bidtimestamp=datetime.datetime.now())
                bid.save()
                return redirect('auctionitem', itemid=itemid)
            else:
        
                messages.warning(request, 'You need to log in to place a bid.')
                return redirect('login')  
     
    
    request.session['warning_message']='Your bid amount is too low.'
    return redirect('auctionitem', itemid=itemid)