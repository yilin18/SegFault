CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255)
);

CREATE TABLE Posts (
    PostID INT PRIMARY KEY,
    UserID INT,
    Content TEXT,
    Timestamp DATETIME,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Comments (
    CommentID INT PRIMARY KEY,
    PostID INT DEFAULT -1,
    UserID INT ,
    Content TEXT,
    Timestamp DATETIME,
    FOREIGN KEY (PostID) REFERENCES Posts(PostID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Likes (
    LikeID INT PRIMARY KEY,
    UserID INT,
    PostID INT NULL DEFAULT -1,
    CommentID INT NULL DEFAULT -1,
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (PostID) REFERENCES Posts(PostID),
    FOREIGN KEY (CommentID) REFERENCES Comments(CommentID)
);

CREATE TABLE Followers (
    FollowerID INT PRIMARY KEY,
    FollowingUserID INT,
    FollowedUserID INT,
    FOREIGN KEY (FollowingUserID) REFERENCES Users(UserID),
    FOREIGN KEY (FollowedUserID) REFERENCES Users(UserID)
);

CREATE TABLE `Groups` (
    GroupID INT PRIMARY KEY,
    Name VARCHAR(255),
    Description TEXT
);

CREATE TABLE GroupMemberships (
    MembershipID INT PRIMARY KEY,
    GroupID INT,
    UserID INT,
    FOREIGN KEY (GroupID) REFERENCES `Groups`(GroupID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/social_media/users.csv'
INTO TABLE Users
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/social_media/posts.csv'
INTO TABLE Posts
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/social_media/comments.csv'
INTO TABLE Comments
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/social_media/likes.csv'
INTO TABLE Likes
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(LikeID, UserID, @vPostID, @vCommentID)
SET PostID = NULLIF(@vPostID, ''),
    CommentID = CASE WHEN TRIM(@vCommentID) REGEXP '^[0-9]+$' THEN @vCommentID ELSE NULL END;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/social_media/followers.csv'
INTO TABLE Followers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/social_media/groups.csv'
INTO TABLE Groups
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/social_media/group_memberships.csv'
INTO TABLE GroupMemberships
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


