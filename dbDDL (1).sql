CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Type ENUM('Normal', 'Admin') NOT NULL
);

CREATE TABLE Categories (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    ParentCategoryID INT,
    FOREIGN KEY (ParentCategoryID) REFERENCES Categories(CategoryID)
);

CREATE TABLE Products (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Description TEXT,
    OwnerID INT,
    CategoryID INT,
    FOREIGN KEY (OwnerID) REFERENCES Users(UserID),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);
CREATE TABLE Auctions (
    AuctionID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT,
    AuctionDate DATETIME NOT NULL,
    Duration INT NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE Bids (
    BidID INT AUTO_INCREMENT PRIMARY KEY,
    Amount DECIMAL(10, 2) NOT NULL,
    AuctionID INT,
    BidderID INT,
    BidTimestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (AuctionID) REFERENCES Auctions(AuctionID),
    FOREIGN KEY (BidderID) REFERENCES Users(UserID)
);

CREATE TABLE AuctionedItems (
    ItemID INT AUTO_INCREMENT PRIMARY KEY,
    AuctionID INT NOT NULL,
    ProductID INT NOT NULL,
    SellerID INT NOT NULL,
    StartingPrice DECIMAL(10, 2) NOT NULL DEFAULT 0,
    FOREIGN KEY (AuctionID) REFERENCES Auctions(AuctionID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    FOREIGN KEY (SellerID) REFERENCES Users(UserID)
);

CREATE TABLE Payments (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    BuyerID INT NOT NULL,
    SellerID INT NOT NULL,
    AuctionedItemID INT,
    PaymentAmount DECIMAL(10, 2) NOT NULL,
    PaymentDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    ModeOfPayment VARCHAR(255),
    PaymentStatus ENUM('Pending', 'Completed', 'Failed') NOT NULL,
    FOREIGN KEY (BuyerID) REFERENCES Users(UserID),
    FOREIGN KEY (SellerID) REFERENCES Users(UserID),
    FOREIGN KEY (AuctionedItemID) REFERENCES AuctionedItems(ItemID)
);

CREATE TABLE Shipments (
    ShipmentID INT AUTO_INCREMENT PRIMARY KEY,
    PaymentID INT NOT NULL,
    ShippingAddress TEXT NOT NULL,
    TrackingID VARCHAR(255),
    Status ENUM('Preparing', 'Shipped', 'In Transit', 'Delivered', 'Delayed', 'Cancelled') NOT NULL,
    ShipmentDate DATETIME,
    EstimatedDeliveryDate DATETIME,
    ActualDeliveryDate DATETIME,
    FOREIGN KEY (PaymentID) REFERENCES Payments(PaymentID)
);


CREATE TABLE Reports (
    ReportID INT AUTO_INCREMENT PRIMARY KEY,
    ReportDate DATETIME NOT NULL,
    ReportQuery TEXT NOT NULL,
    Content TEXT NOT NULL,
    CreatorID INT,
    FOREIGN KEY (CreatorID) REFERENCES Users(UserID)
);

CREATE TABLE Views (
    ViewID INT AUTO_INCREMENT PRIMARY KEY,
    ReportID INT,
    UserID INT,
    ViewDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ReportID) REFERENCES Reports(ReportID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Feedback (
    FeedbackID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    ProdID INT NOT NULL,
    Rating INT NOT NULL,
    Comment TEXT,
    Date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (ProdID) REFERENCES Products(ProductID)
);

CREATE TABLE Message (
    MessageID INT AUTO_INCREMENT PRIMARY KEY,
    SenderID INT NOT NULL,
    ReceiverID INT NOT NULL,
    Content TEXT NOT NULL,
    IsRead BOOLEAN DEFAULT FALSE,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (SenderID) REFERENCES Users(UserID),
    FOREIGN KEY (ReceiverID) REFERENCES Users(UserID)
);

CREATE TABLE AuditLog (
    AuditID INT AUTO_INCREMENT PRIMARY KEY,
    TableName VARCHAR(255) NOT NULL,
    RecordID INT NOT NULL,
    ActionTaken VARCHAR(255) NOT NULL,
    ActionDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Description TEXT
);
DELIMITER $$
CREATE TRIGGER AfterPaymentStatusChange
AFTER UPDATE ON Payments
FOR EACH ROW
BEGIN
    IF OLD.PaymentStatus <> 'Completed' AND NEW.PaymentStatus = 'Completed' THEN
        INSERT INTO AuditLog (TableName, RecordID, ActionTaken, Description)
        VALUES ('Payments', NEW.PaymentID, 'Update', CONCAT('Payment status changed to Completed for PaymentID: ', NEW.PaymentID));
    END IF;
END$$
DELIMITER ;

DELIMITER $$

CREATE TRIGGER NotifySellerOnSale
AFTER UPDATE ON Payments
FOR EACH ROW
BEGIN
    IF OLD.PaymentStatus <> 'Completed' AND NEW.PaymentStatus = 'Completed' THEN
        INSERT INTO Message (SenderID, ReceiverID, Content, IsRead)
        SELECT NEW.BuyerID, NEW.SellerID, CONCAT('Your item associated with PaymentID ', NEW.PaymentID, ' has been sold.'), FALSE
        FROM dual
        WHERE NOT EXISTS (
            SELECT * FROM Message WHERE PaymentID = NEW.PaymentID AND Content LIKE '%has been sold%'
        );
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE TRIGGER NotifySellerOnSale
AFTER UPDATE ON Payments
FOR EACH ROW
BEGIN
    IF OLD.PaymentStatus <> 'Completed' AND NEW.PaymentStatus = 'Completed' THEN
        INSERT INTO Message (SenderID, ReceiverID, Content, IsRead)
        SELECT NEW.BuyerID, NEW.SellerID, CONCAT('Your item associated with PaymentID ', NEW.PaymentID, ' has been sold.'), FALSE
        FROM dual
        WHERE NOT EXISTS (
            SELECT * FROM Message WHERE PaymentID = NEW.PaymentID AND Content LIKE '%has been sold%'
        );
    END IF;
END$$

DELIMITER ;

DELIMITER $$

CREATE PROCEDURE ProcessNewBid(
    IN bidAmount DECIMAL(10,2),
    IN auctionID INT,
    IN bidderID INT
)
BEGIN
    DECLARE startingPrice DECIMAL(10,2);
    DECLARE auctionItemID INT;
    DECLARE currentHighestBid DECIMAL(10,2); -- Moved up to be declared at the beginning

    -- Retrieve the AuctionedItemID and starting price for the auction
    SELECT ItemID, StartingPrice INTO auctionItemID, startingPrice
    FROM AuctionedItems
    WHERE AuctionID = auctionID;

    IF auctionItemID IS NOT NULL THEN
        -- Check if the bid is at least the starting price
        IF bidAmount >= startingPrice THEN
            -- Check if this is the first bid for the auction
            IF NOT EXISTS (SELECT 1 FROM Bids WHERE AuctionID = auctionID) THEN
                INSERT INTO Bids (Amount, AuctionID, BidderID)
                VALUES (bidAmount, auctionID, bidderID);
            ELSE
                SELECT MAX(Amount) INTO currentHighestBid FROM Bids WHERE AuctionID = auctionID;
                IF bidAmount > currentHighestBid THEN
                    INSERT INTO Bids (Amount, AuctionID, BidderID)
                    VALUES (bidAmount, auctionID, bidderID);
                ELSE
                    -- Optionally, handle the case where the new bid is not higher than the current highest bid
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Bid must be higher than the current highest bid.';
                END IF;
            END IF;
        ELSE
            -- Handle the case where the bid is lower than the starting price
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Bid must be at least the starting price of the auction.';
        END IF;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Auction item not found.';
    END IF;
END$$

DELIMITER ;


CREATE VIEW AuctionDetails AS
SELECT 
    a.AuctionID,
    p.Name AS ProductName,
    p.Description,
    MAX(b.Amount) AS HighestBid,
    u.Name AS SellerName,
    ai.StartingPrice,
    a.AuctionDate,
    a.Duration
FROM Auctions a
JOIN AuctionedItems ai ON a.AuctionID = ai.AuctionID
JOIN Products p ON ai.ProductID = p.ProductID
JOIN Users u ON p.OwnerID = u.UserID
LEFT JOIN Bids b ON a.AuctionID = b.AuctionID
GROUP BY a.AuctionID
ORDER BY a.AuctionDate DESC;
