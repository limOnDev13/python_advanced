SELECT DISTINCT maker as Maker
FROM Product
WHERE (type = 'PC') AND (model IN (SELECT model FROM PC WHERE speed >= 450))