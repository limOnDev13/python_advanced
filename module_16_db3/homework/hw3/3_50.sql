SELECT DISTINCT battle
FROM outcomes
JOIN ships ON outcomes.ship = ships.name AND ships.class = 'Kongo'