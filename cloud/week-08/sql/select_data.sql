SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName 
FROM ProductCategory pc 
JOIN Product p 
ON pc.productcategoryid = p.productcategoryid;