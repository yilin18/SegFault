from constants import *


# mysql queries
mysql_short_queries = [
    """SELECT * FROM Users WHERE UserID = 123;""",
    """SELECT * FROM Products WHERE ProductID = 456;
    """,
    """SELECT * FROM Categories;
    """,
    """SELECT * FROM Orders WHERE Date = '2023-01-01';
    """,
    """SELECT * FROM OrderDetails WHERE OrderID = 789;
    """,
]

mysql_long_queries = [
    """SELECT Users.Name, Users.Email, Orders.OrderID, Orders.Date, Orders.Status 
    FROM Users 
    JOIN Orders ON Users.UserID = Orders.UserID 
    WHERE Users.UserID = 123 AND Orders.Date >= '2023-01-01';
    """,
    """SELECT p.ProductID, p.Name, p.Description 
    FROM Products p 
    JOIN OrderDetails od ON p.ProductID = od.ProductID 
    JOIN Orders o ON od.OrderID = o.OrderID 
    WHERE o.UserID = 123;
    """,
    """SELECT DISTINCT u.UserID, u.Name 
    FROM Users u 
    JOIN Orders o ON u.UserID = o.UserID 
    JOIN OrderDetails od ON o.OrderID = od.OrderID 
    WHERE od.ProductID = 456;
    """,
    """SELECT o.OrderID, p.ProductID, p.Name 
    FROM Orders o 
    JOIN OrderDetails od ON o.OrderID = od.OrderID 
    JOIN Products p ON od.ProductID = p.ProductID 
    JOIN Categories c ON p.CategoryID = c.CategoryID 
    WHERE c.Name = 'Electronics';
    """,
    """SELECT p.ProductID, p.Name 
    FROM Products p 
    WHERE p.ProductID NOT IN (
        SELECT od.ProductID 
        FROM OrderDetails od 
        JOIN Orders o ON od.OrderID = o.OrderID 
        WHERE o.UserID = 123
    );
    """,
    """SELECT o.OrderID, COUNT(od.ProductID) as ProductCount 
    FROM Orders o 
    JOIN OrderDetails od ON o.OrderID = od.OrderID 
    GROUP BY o.OrderID 
    HAVING COUNT(od.ProductID) > 3;
    """,
]

mysql_aggregated_queries = [
    """SELECT Categories.Name, COUNT(Orders.OrderID) as OrderCount 
    FROM Orders 
    JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID 
    JOIN Products ON OrderDetails.ProductID = Products.ProductID 
    JOIN Categories ON Products.CategoryID = Categories.CategoryID 
    WHERE Orders.UserID = 123 
    GROUP BY Categories.CategoryID;
    """,
    """SELECT od1.ProductID, od2.ProductID, COUNT(*) AS Frequency 
    FROM OrderDetails od1 
    JOIN OrderDetails od2 ON od1.OrderID = od2.OrderID AND od1.ProductID < od2.ProductID 
    GROUP BY od1.ProductID, od2.ProductID 
    ORDER BY Frequency DESC 
    LIMIT 10;
    """,
    """SELECT Users.UserID, Users.Name, SUM(Orders.TotalPrice) as TotalSpent 
    FROM Users 
    JOIN Orders ON Users.UserID = Orders.UserID 
    GROUP BY Users.UserID 
    HAVING TotalSpent > 1000;
    """,
    """SELECT c.CategoryID, c.Name, AVG(p.Price) AS AveragePrice
    FROM Categories c
    JOIN Products p ON c.CategoryID = p.CategoryID
    GROUP BY c.CategoryID;
    """,
    """SELECT DATE(o.Date) AS OrderDate, COUNT(o.OrderID) AS OrderCount
    FROM Orders o
    GROUP BY DATE(o.Date);
    """,
    """SELECT p.ProductID, p.Name, COUNT(od.OrderID) AS OrdersCount
    FROM Products p
    JOIN OrderDetails od ON p.ProductID = od.ProductID
    GROUP BY p.ProductID
    ORDER BY OrdersCount DESC
    LIMIT 5;
    """,
]

mysql_nested_queries = [
    """SELECT p.ProductID, p.Name 
    FROM Products p 
    WHERE NOT EXISTS (
        SELECT * 
        FROM OrderDetails od 
        WHERE od.ProductID = p.ProductID
    );
    """,
    """SELECT u.UserID, u.Name 
    FROM Users u 
    WHERE EXISTS (
        SELECT * 
        FROM Orders o 
        WHERE o.UserID = u.UserID AND o.TotalPrice > (
            SELECT AVG(o2.TotalPrice) 
            FROM Orders o2
        )
    );
    """,
    """SELECT c.CategoryID, c.Name 
    FROM Categories c 
    WHERE (
        SELECT COUNT(p.ProductID) 
        FROM Products p 
        WHERE p.CategoryID = c.CategoryID
    ) > (
        SELECT AVG(ProductCount) 
        FROM (
            SELECT COUNT(p2.ProductID) AS ProductCount 
            FROM Products p2 
            GROUP BY p2.CategoryID
        ) AS SubQuery
    );
    """,
    """SELECT c.CategoryID, c.Name
    FROM Categories c
    WHERE (
        SELECT SUM(p.Price * od.Quantity)
        FROM Products p
        JOIN OrderDetails od ON p.ProductID = od.ProductID
        WHERE p.CategoryID = c.CategoryID
    ) > (
        SELECT AVG(CategorySales) FROM (
            SELECT SUM(p.Price * od.Quantity) AS CategorySales
            FROM Products p
            JOIN OrderDetails od ON p.ProductID = od.ProductID
            JOIN Categories c_inner ON p.CategoryID = c_inner.CategoryID
            GROUP BY c_inner.CategoryID
        ) AS SubQuery
    );
    """,
    """SELECT u.UserID, u.Name 
    FROM Users u 
    WHERE NOT EXISTS (
        SELECT * 
        FROM Orders o 
        WHERE o.UserID = u.UserID AND o.TotalPrice > 100
    );
    """,
]

# neo4j queries
neo4j_short_queries = [
    """MATCH (u:User) WHERE u.UserID = 123 RETURN u;""",
    """MATCH (p:Product {ProductID: 456}) RETURN p;""",
    """MATCH (c:Category) RETURN c;
    """,
    """MATCH (o:Order {Date: '2023-01-01'}) RETURN o;
    """,
    """MATCH (o:Order {OrderID: 789})-[:CONTAINS]->(od:OrderDetails) RETURN od;
    """,
]

neo4j_long_queries = [
    """MATCH (u:User {UserID: 123})-[:PLACED]->(o:Order) 
    WHERE o.Date >= '2023-01-01' 
    RETURN u.Name, u.Email, o.OrderID, o.Date, o.Status;
    """,
    """MATCH (u:User {UserID: 123})-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product) 
    RETURN p.ProductID, p.Name, p.Description;
    """,
    """MATCH (u:User)-[:PLACED]->(:Order)-[:CONTAINS]->(p:Product {ProductID: 456}) 
    RETURN DISTINCT u.UserID, u.Name;
    """,
    """MATCH (c:Category {Name: 'Electronics'})<-[:BELONGS_TO]-(p:Product)<-[:CONTAINS]-(o:Order) 
    RETURN o.OrderID, p.ProductID, p.Name;
    """,
    """MATCH (p:Product) 
    WHERE NOT (p)<-[:CONTAINS]-(:Order)-[:PLACED]->(:User {UserID: 123}) 
    RETURN p.ProductID, p.Name;
    """,
    """MATCH (o:Order)-[:CONTAINS]->(p:Product) 
    WITH o, COUNT(p) AS ProductCount 
    WHERE ProductCount > 3 
    RETURN o.OrderID, ProductCount;
    """,
]

neo4j_aggregated_queries = [
    """MATCH (u:User {UserID: 123})-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product)-[:BELONGS_TO]->(c:Category) 
    RETURN c.Name, COUNT(o) AS OrderCount;
    """,
    """MATCH (p1:Product)<-[:CONTAINS]-(o:Order)-[:CONTAINS]->(p2:Product) 
    WHERE ID(p1) < ID(p2) 
    RETURN p1.ProductID, p2.ProductID, COUNT(*) AS Frequency 
    ORDER BY Frequency DESC 
    LIMIT 10;
    """,
    """MATCH (u:User)-[:PLACED]->(o:Order) 
    WITH u, SUM(o.TotalPrice) AS TotalSpent 
    WHERE TotalSpent > 1000 
    RETURN u.UserID, u.Name, TotalSpent;
    """,
    """MATCH (c:Category)<-[:BELONGS_TO]-(p:Product)
    RETURN c.CategoryID, c.Name, AVG(p.Price) AS AveragePrice;
    """,
    """MATCH (o:Order)
    RETURN DATE(o.Date) AS OrderDate, COUNT(o) AS OrderCount;
    """,
    """MATCH (p:Product)<-[:CONTAINS]-(:Order)
    RETURN p.ProductID, p.Name, COUNT(*) AS OrdersCount
    ORDER BY OrdersCount DESC
    LIMIT 5;
    """,
]

neo4j_nested_queries = [
    """MATCH (p:Product) 
    WHERE NOT (p)<-[:CONTAINS]-(:Order) 
    RETURN p.ProductID, p.Name;
    """,
    """MATCH (o:Order)
    WITH AVG(o.TotalPrice) AS AvgPrice
    MATCH (u:User)-[:PLACED]->(o:Order)
    WHERE o.TotalPrice > AvgPrice
    RETURN u.UserID, u.Name;
    """,
    """MATCH (c:Category)<-[:BELONGS_TO]-(p:Product)
    WITH c, COUNT(p) AS ProductCount
    WITH AVG(ProductCount) AS AvgProductCount
    MATCH (c:Category)<-[:BELONGS_TO]-(p:Product)
    WITH c, COUNT(p) AS ProductCount, AvgProductCount
    WHERE ProductCount > AvgProductCount
    RETURN c.CategoryID, c.Name;
    """,
    """MATCH (c:Category)<-[:BELONGS_TO]-(p:Product)<-[:CONTAINS]-(od:OrderDetails)
    WITH c, SUM(p.Price * od.Quantity) AS CategorySales
    WITH AVG(CategorySales) AS AvgCategorySales
    MATCH (c:Category)<-[:BELONGS_TO]-(p:Product)<-[:CONTAINS]-(od:OrderDetails)
    WITH c, SUM(p.Price * od.Quantity) AS CategorySales, AvgCategorySales
    WHERE CategorySales > AvgCategorySales
    RETURN c.CategoryID, c.Name;
    """,
    """MATCH (u:User)-[:PLACED]->(o:Order) 
    WITH u, MAX(o.TotalPrice) AS MaxPrice 
    WHERE MaxPrice <= 100 
    RETURN u.UserID, u.Name;
    """,
]


transcation_queries_by_type_and_db = {
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
