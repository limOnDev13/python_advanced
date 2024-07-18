SELECT model, price
FROM PC WHERE PC.model IN (SELECT model FROM Product WHERE maker = 'B')
UNION SELECT model, price
FROM Laptop WHERE Laptop.model IN (SELECT model FROM Product WHERE maker = 'B')
UNION SELECT model, price
FROM Printer WHERE Printer.model IN (SELECT model FROM Product WHERE maker = 'B')