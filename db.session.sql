-- customer name header
-- seller names as bulleted list

SELECT
    c.id as customer_id,
    a.first_name || ' ' || a.last_name as customer_name,
    b.first_name || ' ' || b.last_name as seller_name
FROM bangazonapi_favorite f
JOIN bangazonapi_customer c ON c.id = f.customer_id
JOIN auth_user a ON c.user_id = a.id
JOIN bangazonapi_customer d ON d.id = f.seller_id
JOIN auth_user b ON d.user_id = b.id