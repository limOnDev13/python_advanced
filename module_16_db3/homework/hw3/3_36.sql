SELECT name FROM ships WHERE name = class
UNION
SELECT ship AS name FROM outcomes
WHERE ship IN (SELECT DISTINCT class FROM classes)