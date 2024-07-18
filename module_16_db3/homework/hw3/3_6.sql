SELECT DISTINCT Product.maker, Laptop.speed
FROM Product, Laptop
WHERE ((Laptop.hd >= 10) AND (Product.model = laptop.model))