-- customer name header
-- seller names as bulleted list

SELECT *
    -- first_name || ' ' || last_name as fullname
FROM auth_user 
JOIN bangazonapi_customer c ON c.user_id = auth_user.id
JOIN bangazonapi_favorite f ON f.customer_id = c.id