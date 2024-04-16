# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Auctioneditems(models.Model):
    itemid = models.AutoField(db_column='ItemID', primary_key=True)  # Field name made lowercase.
    auctionid = models.ForeignKey('Auctions', models.DO_NOTHING, db_column='AuctionID')  # Field name made lowercase.
    productid = models.ForeignKey('Products', models.DO_NOTHING, db_column='ProductID')  # Field name made lowercase.
    sellerid = models.ForeignKey('Users', models.DO_NOTHING, db_column='SellerID')  # Field name made lowercase.
    startingprice = models.IntegerField(db_column="StartingPrice")
    class Meta:
        #managed = False
        db_table = 'AuctionedItems'


class Auctions(models.Model):
    auctionid = models.AutoField(db_column='AuctionID', primary_key=True)  # Field name made lowercase.
    productid = models.ForeignKey('Products', models.DO_NOTHING, db_column='ProductID', blank=True, null=True)  # Field name made lowercase.
    auctiondate = models.DateTimeField(db_column='AuctionDate')  # Field name made lowercase.
    duration = models.IntegerField(db_column='Duration')  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Auctions'


class Bids(models.Model):
    bidid = models.AutoField(db_column='BidID', primary_key=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2)  # Field name made lowercase.
    itemid = models.ForeignKey('AuctionedItems', models.DO_NOTHING, db_column='ItemID', blank=True, null=True) 
    bidderid = models.ForeignKey('Users', models.DO_NOTHING, db_column='BidderID', blank=True, null=True)  # Field name made lowercase.
    bidtimestamp = models.DateTimeField(db_column='BidTimestamp', blank=True, null=True)  # Field name made lowercase.
     # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Bids'


class Categories(models.Model):
    categoryid = models.AutoField(db_column='CategoryID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    parentcategoryid = models.ForeignKey('self', models.DO_NOTHING, db_column='ParentCategoryID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Categories'


class Feedback(models.Model):
    feedbackid = models.AutoField(db_column='FeedbackID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID')  # Field name made lowercase.
    prodid = models.ForeignKey('Products', models.DO_NOTHING, db_column='ProdID')  # Field name made lowercase.
    rating = models.IntegerField(db_column='Rating')  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Feedback'


class Message(models.Model):
    messageid = models.AutoField(db_column='MessageID', primary_key=True)  # Field name made lowercase.
    senderid = models.ForeignKey('Users', models.DO_NOTHING, db_column='SenderID')  # Field name made lowercase.
    receiverid = models.ForeignKey('Users', models.DO_NOTHING, db_column='ReceiverID', related_name='message_receiverid_set')  # Field name made lowercase.
    content = models.TextField(db_column='Content')  # Field name made lowercase.
    isread = models.IntegerField(db_column='IsRead', blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column='Timestamp', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Message'


class Payments(models.Model):
    paymentid = models.AutoField(db_column='PaymentID', primary_key=True)  # Field name made lowercase.
    buyerid = models.ForeignKey('Users', models.DO_NOTHING, db_column='BuyerID')  # Field name made lowercase.
    sellerid = models.ForeignKey('Users', models.DO_NOTHING, db_column='SellerID', related_name='payments_sellerid_set')  # Field name made lowercase.
    auctioneditemid = models.ForeignKey(Auctioneditems, models.DO_NOTHING, db_column='AuctionedItemID', blank=True, null=True)  # Field name made lowercase.
    paymentamount = models.DecimalField(db_column='PaymentAmount', max_digits=10, decimal_places=2)  # Field name made lowercase.
    paymentdate = models.DateTimeField(db_column='PaymentDate', blank=True, null=True)  # Field name made lowercase.
    modeofpayment = models.CharField(db_column='ModeOfPayment', max_length=255, blank=True, null=True)  # Field name made lowercase.
    paymentstatus = models.CharField(db_column='PaymentStatus', max_length=9)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Payments'


class Products(models.Model):
    productid = models.AutoField(db_column='ProductID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    ownerid = models.ForeignKey('Users', models.DO_NOTHING, db_column='OwnerID', blank=True, null=True)  # Field name made lowercase.
    categoryid = models.ForeignKey(Categories, models.DO_NOTHING, db_column='CategoryID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Products'


class Reports(models.Model):
    reportid = models.AutoField(db_column='ReportID', primary_key=True)  # Field name made lowercase.
    reportdate = models.DateTimeField(db_column='ReportDate')  # Field name made lowercase.
    reportquery = models.TextField(db_column='ReportQuery')  # Field name made lowercase.
    content = models.TextField(db_column='Content')  # Field name made lowercase.
    creatorid = models.ForeignKey('Users', models.DO_NOTHING, db_column='CreatorID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Reports'


class Shipments(models.Model):
    shipmentid = models.AutoField(db_column='ShipmentID', primary_key=True)  # Field name made lowercase.
    paymentid = models.ForeignKey(Payments, models.DO_NOTHING, db_column='PaymentID')  # Field name made lowercase.
    shippingaddress = models.TextField(db_column='ShippingAddress')  # Field name made lowercase.
    trackingid = models.CharField(db_column='TrackingID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=10)  # Field name made lowercase.
    shipmentdate = models.DateTimeField(db_column='ShipmentDate', blank=True, null=True)  # Field name made lowercase.
    estimateddeliverydate = models.DateTimeField(db_column='EstimatedDeliveryDate', blank=True, null=True)  # Field name made lowercase.
    actualdeliverydate = models.DateTimeField(db_column='ActualDeliveryDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Shipments'


class Users(models.Model):
    userid = models.AutoField(db_column='UserID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=255)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=6)  # Field name made lowercase.

    class Meta:
       # managed = False
        db_table = 'Users'


class Views(models.Model):
    viewid = models.AutoField(db_column='ViewID', primary_key=True)  # Field name made lowercase.
    reportid = models.ForeignKey(Reports, models.DO_NOTHING, db_column='ReportID', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey(Users, models.DO_NOTHING, db_column='UserID', blank=True, null=True)  # Field name made lowercase.
    viewdate = models.DateTimeField(db_column='ViewDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'Views'



