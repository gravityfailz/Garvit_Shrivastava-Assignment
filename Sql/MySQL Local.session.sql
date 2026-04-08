SELECT customer_id,
SUM(total_amount) AS total_spent,
RANK() OVER (ORDER BY SUM(total_amount) DESC) AS ranking
FROM Orders
GROUP BY customer_id;