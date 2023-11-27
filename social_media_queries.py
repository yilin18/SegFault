from constants import *


# mysql queries
mysql_short_queries = [
    """SELECT * FROM Posts WHERE UserID = 123;""",
    """SELECT * FROM Posts WHERE PostID = 456;
    """,
    """SELECT * FROM Comments WHERE PostID = 789;
    """,
    """SELECT * FROM Likes WHERE PostID = 1011;
    """,
    """SELECT u.UserID, u.Name 
    FROM Users u 
    JOIN GroupMemberships gm ON u.UserID = gm.UserID 
    WHERE gm.GroupID = 202;
    """,
]

mysql_long_queries = [
    """SELECT DISTINCT u.UserID, u.Name 
    FROM Users u 
    JOIN Comments c ON u.UserID = c.UserID 
    WHERE c.PostID = 456;
    """,
    """SELECT f.FollowedUserID, u.Name 
    FROM Followers f 
    JOIN Users u ON f.FollowedUserID = u.UserID 
    WHERE f.FollowingUserID = 123;
    """,
    """SELECT u.UserID, u.Name 
    FROM Users u 
    JOIN GroupMemberships gm ON u.UserID = gm.UserID 
    WHERE gm.GroupID = 789;
    """,
    """SELECT DISTINCT u2.UserID, u2.Name 
    FROM Likes l1 
    JOIN Likes l2 ON l1.PostID = l2.PostID AND l1.UserID != l2.UserID 
    JOIN Users u2 ON l2.UserID = u2.UserID 
    WHERE l1.UserID = 123;
    """,
    """SELECT DISTINCT u2.UserID, u2.Name 
    FROM Users u1 
    JOIN Followers f ON u1.UserID = f.FollowingUserID 
    JOIN Posts p ON f.FollowedUserID = p.UserID 
    JOIN Comments c ON p.PostID = c.PostID 
    JOIN Users u2 ON c.UserID = u2.UserID 
    WHERE u1.UserID = 123;
    """
]

mysql_aggregated_queries = [
    """SELECT p.PostID, p.Content, p.Timestamp, COUNT(l.LikeID) as LikeCount
    FROM Posts p
    LEFT JOIN Likes l ON p.PostID = l.PostID
    WHERE p.PostID IN (
        SELECT MAX(p2.PostID)
        FROM Posts p2
        GROUP BY p2.UserID
    )
    GROUP BY p.PostID;
    """,
    """SELECT u.UserID, u.Name, COUNT(f.FollowerID) as FollowerCount, COUNT(p.PostID) as PostCount
    FROM Users u
    LEFT JOIN Followers f ON u.UserID = f.FollowedUserID
    LEFT JOIN Posts p ON u.UserID = p.UserID
    GROUP BY u.UserID
    ORDER BY FollowerCount DESC, PostCount DESC
    LIMIT 5;
    """,
    """SELECT u.UserID, u.Name, COUNT(p.PostID) AS PostCount 
    FROM Users u 
    JOIN Posts p ON u.UserID = p.UserID 
    GROUP BY u.UserID;
    """,
    """SELECT AVG(CommentCount) AS AvgCommentsPerPost 
    FROM (
        SELECT p.PostID, COUNT(c.CommentID) AS CommentCount 
        FROM Posts p 
        LEFT JOIN Comments c ON p.PostID = c.PostID 
        GROUP BY p.PostID
    ) AS SubQuery;
    """,
    """SELECT p.PostID, COUNT(l.LikeID) AS LikeCount 
    FROM Posts p 
    LEFT JOIN Likes l ON p.PostID = l.PostID 
    GROUP BY p.PostID;
    """,
    """SELECT g.GroupID, g.Name, COUNT(gm.UserID) AS UserCount 
    FROM `Groups` g 
    JOIN GroupMemberships gm ON g.GroupID = gm.GroupID 
    GROUP BY g.GroupID;
    """,
]

mysql_nested_queries = [
    """SELECT u.UserID, u.Name 
    FROM Users u 
    WHERE (
        SELECT COUNT(p.PostID) 
        FROM Posts p 
        WHERE p.UserID = u.UserID
    ) > (
        SELECT AVG(PostCount) 
        FROM (
            SELECT COUNT(p.PostID) AS PostCount 
            FROM Posts p 
            GROUP BY p.UserID
        ) AS SubQuery
    );
    """,
    """SELECT p.PostID 
    FROM Posts p 
    WHERE (
        SELECT COUNT(l.LikeID) 
        FROM Likes l 
        WHERE l.PostID = p.PostID
    ) > (
        SELECT AVG(LikeCount) 
        FROM (
            SELECT COUNT(l.LikeID) AS LikeCount 
            FROM Likes l 
            GROUP BY l.PostID
        ) AS SubQuery
    );
    """,
    """SELECT u.UserID, u.Name 
    FROM Users u 
    WHERE (
        SELECT COUNT(c.CommentID) 
        FROM Comments c 
        WHERE c.UserID = u.UserID
    ) > (
        SELECT COUNT(p.PostID) 
        FROM Posts p 
        WHERE p.UserID = u.UserID
    );
    """,
    """SELECT u.UserID, u.Name 
    FROM Users u 
    WHERE NOT EXISTS (
        SELECT * 
        FROM Likes l 
        WHERE l.UserID = u.UserID
    );
    """,
    """SELECT p.PostID 
    FROM Posts p 
    WHERE NOT EXISTS (
        SELECT * 
        FROM Comments c 
        WHERE c.PostID = p.PostID
    );
    """,
]

# neo4j queries
neo4j_short_queries = [
    """MATCH (u:User {UserID: 123})-[:CREATED]->(p:Post) RETURN p;""",
    """MATCH (p:Post {PostID: 456}) RETURN p;
    """,
    """MATCH (:Post {PostID: 789})<-[:COMMENTED]-(c:Comment) RETURN c;
    """,
    """MATCH (:Post {PostID: 1011})<-[:LIKED]-(l:Like) RETURN l;
    """,
    """MATCH (:Group {GroupID: 202})<-[:MEMBER_OF]-(u:User) 
    RETURN u.UserID, u.Name;
    """,
]

neo4j_long_queries = [
    """MATCH (u:User)-[:COMMENTED]->(c:Comment)-[:ON]->(p:Post {PostID: 456}) 
    RETURN DISTINCT u.UserID, u.Name;
    """,
    """MATCH (u:User {UserID: 123})-[:FOLLOWS]->(f:User) 
    RETURN f.UserID, f.Name;
    """,
    """MATCH (u:User)-[:MEMBER_OF]->(g:Group {GroupID: 789}) 
    RETURN u.UserID, u.Name;
    """,
    """MATCH (u1:User {UserID: 123})-[:LIKES]->(p:Post)<-[:LIKES]-(u2:User)
    WHERE u1 <> u2
    RETURN DISTINCT u2.UserID, u2.Name;
    """,
    """MATCH (u1:User {UserID: 123})-[:FOLLOWS]->(u2:User)-[:CREATED]->(p:Post)<-[:COMMENTED]-(u3:User)
    RETURN DISTINCT u3.UserID, u3.Name;
    """,
]

neo4j_aggregated_queries = [
    """MATCH (u:User)-[:CREATED]->(p:Post)
    WITH u, p, MAX(p.Timestamp) AS LatestPost
    MATCH (p2:Post {Timestamp: LatestPost})<-[:CREATED]-(u)
    OPTIONAL MATCH (p2)<-[:LIKES]-(l:Like)
    RETURN p2.PostID, p2.Content, p2.Timestamp, COUNT(l) AS LikeCount;
    """,
    """MATCH (u:User)
    OPTIONAL MATCH (u)<-[:FOLLOWS]-(f:User)
    OPTIONAL MATCH (u)-[:CREATED]->(p:Post)
    RETURN u.UserID, u.Name, COUNT(DISTINCT f) AS FollowerCount, COUNT(p) AS PostCount
    ORDER BY FollowerCount DESC, PostCount DESC
    LIMIT 5;
    """,
    """MATCH (u:User)-[:CREATED]->(p:Post) 
    RETURN u.UserID, u.Name, COUNT(p) AS PostCount;
    """,
    """MATCH (p:Post)<-[:COMMENTED]-(c:Comment) 
    WITH p, COUNT(c) AS CommentCount 
    RETURN AVG(CommentCount) AS AvgCommentsPerPost;
    """,
    """MATCH (p:Post)<-[:LIKED]-(l:Like) 
    RETURN p.PostID, COUNT(l) AS LikeCount;
    """,
    """MATCH (g:Group)<-[:MEMBER_OF]-(u:User) 
    RETURN g.GroupID, g.Name, COUNT(u) AS UserCount;
    """,
]

neo4j_nested_queries = [
    """MATCH (u:User)-[:CREATED]->(p:Post)
    WITH u, COUNT(p) AS UserPostCount
    WITH COLLECT({user: u, postCount: UserPostCount}) AS UsersPosts, 
        AVG(UserPostCount) AS AvgPostCount
    UNWIND UsersPosts AS UserPost
    WITH UserPost.user AS User, UserPost.postCount AS PostCount, AvgPostCount
    WHERE PostCount > AvgPostCount
    RETURN User.UserID, User.Name;
    """,
    """MATCH (p:Post)
    OPTIONAL MATCH (p)<-[:LIKED]-(l:Like)
    WITH p, COUNT(l) AS LikesCount
    WITH COLLECT({post: p, likes: LikesCount}) AS PostsLikes, 
        AVG(LikesCount) AS AvgLikes
    UNWIND PostsLikes AS PostLike
    WITH PostLike.post AS Post, PostLike.likes AS LikesCount, AvgLikes
    WHERE LikesCount > AvgLikes
    RETURN Post.PostID, LikesCount;
    """,
    """MATCH (u:User)
    OPTIONAL MATCH (u)-[:CREATED]->(p:Post)
    WITH u, COUNT(p) AS PostCount
    OPTIONAL MATCH (u)-[:COMMENTED]->(c:Comment)
    WITH u, PostCount, COUNT(c) AS CommentCount
    WHERE CommentCount > PostCount
    RETURN u.UserID, u.Name;
    """,
    """MATCH (u:User) 
    WHERE NOT (u)-[:LIKED]->(:Post) 
    RETURN u.UserID, u.Name;
    """,
    """MATCH (p:Post) 
    WHERE NOT (p)<-[:COMMENTED]-(:User) 
    RETURN p.PostID;
    """
]


social_medial_queries_by_type_and_db = {
    SHORT: {
        MYSQL: mysql_short_queries,
        NEO4J: neo4j_short_queries
    },
    LONG: {
        MYSQL: mysql_long_queries,
        NEO4J: neo4j_long_queries
    },
    AGGREGATED: {
        MYSQL: mysql_aggregated_queries,
        NEO4J: neo4j_aggregated_queries
    },
    NESTED: {
        MYSQL: mysql_nested_queries,
        NEO4J: neo4j_nested_queries
    },
}