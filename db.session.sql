SELECT 
    b_o.id as order_id,
    a.first_name ||' '|| a.last_name as customer_name,
    c.id as customer_id,
    pay.id as payment_type_id,
    pay.merchant_name as payment_card_type,
    SUM(p.price) as order_total
FROM bangazonapi_order b_o
INNER JOIN bangazonapi_customer c ON c.id = b_o.customer_id
INNER JOIN auth_user a ON a.id = c.user_id
INNER JOIN bangazonapi_payment pay ON pay.id = b_o.payment_type_id 
LEFT JOIN bangazonapi_orderproduct op ON op.order_id = b_o.id
LEFT JOIN bangazonapi_product p ON p.id = op.product_id
WHERE b_o.payment_type_id IS NOT NULL
GROUP BY b_o.id