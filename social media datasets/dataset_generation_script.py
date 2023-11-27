import csv
import random
from faker import Faker

# Initialize Faker for generating fake data
fake = Faker()

# Define the number of records
num_users = 5000
num_posts = 20000
num_comments = 50000
num_likes = 100000
num_followers = 25000
num_groups = 1000
num_group_memberships = 15000

# Generate Users
users = [{"UserID": i, "Name": fake.name(), "Email": fake.email()} for i in range(num_users)]

# Generate Posts
posts = [{"PostID": i, "UserID": random.randint(0, num_users - 1), "Content": fake.text(), "Timestamp": fake.date_time()} for i in range(num_posts)]

# Generate Comments
comments = [{"CommentID": i, "PostID": random.randint(0, num_posts - 1), "UserID": random.randint(0, num_users - 1), "Content": fake.sentence(), "Timestamp": fake.date_time()} for i in range(num_comments)]

# Generate Likes (for both posts and comments)
likes = [{"LikeID": i, "UserID": random.randint(0, num_users - 1), "PostID": random.choice([None, random.randint(0, num_posts - 1)]), "CommentID": random.choice([None, random.randint(0, num_comments - 1)])} for i in range(num_likes)]

# Generate Followers (user-user relationships)
followers = [{"FollowerID": i, "FollowingUserID": random.randint(0, num_users - 1), "FollowedUserID": random.randint(0, num_users - 1)} for i in range(num_followers)]

# Generate Groups
groups = [{"GroupID": i, "Name": fake.word(), "Description": fake.sentence()} for i in range(num_groups)]

# Generate Group Memberships
group_memberships = [{"MembershipID": i, "GroupID": random.randint(0, num_groups - 1), "UserID": random.randint(0, num_users - 1)} for i in range(num_group_memberships)]

# Function to write data to CSV
def write_to_csv(filename, fieldnames, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Write data to CSV files
write_to_csv('users.csv', ['UserID', 'Name', 'Email'], users)
write_to_csv('posts.csv', ['PostID', 'UserID', 'Content', 'Timestamp'], posts)
write_to_csv('comments.csv', ['CommentID', 'PostID', 'UserID', 'Content', 'Timestamp'], comments)
write_to_csv('likes.csv', ['LikeID', 'UserID', 'PostID', 'CommentID'], likes)
write_to_csv('followers.csv', ['FollowerID', 'FollowingUserID', 'FollowedUserID'], followers)
write_to_csv('groups.csv', ['GroupID', 'Name', 'Description'], groups)
write_to_csv('group_memberships.csv', ['MembershipID', 'GroupID', 'UserID'], group_memberships)

print("Data generation complete. CSV files created.")
