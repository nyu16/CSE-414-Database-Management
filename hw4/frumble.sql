-- 4.1
CREATE TABLE Sales(
  name VARCHAR(100),
  discount INT,
  month VARCHAR(3),
  price INT);

-- 4.2

-- name -> discount, false functional dependency as different discount values exist for the same name
SELECT * FROM sales s1, sales s2
WHERE s1.name = s2.name and s1.discount != s2.discount;

-- name -> price
SELECT * FROM sales s1, sales s2
WHERE s1.name = s2.name and s1.price != s2.price;

-- month -> discount
SELECT * FROM sales s1, sales s2
WHERE s1.month = s2.month and s1.discount != s2.discount;

-- month -> discount, name -> price, therefore month, price -> discount, price
SELECT * FROM sales s1, sales s2
WHERE s1.name = s2.name and s1.month = s2.month and
s1.discount != s2.discount and s1.price != s2.price;

-- price, month -> name, discount
SELECT * FROM sales s1, sales s2
WHERE s1.price = s2.price and s1.month = s2.month and
s1.name != s2.name and s1.discount != s2.discount;

-- name, discount -> month, price
SELECT * FROM sales s1, sales s2
WHERE s1.name = s2.name and s1.discount = s2.discount and
s1.month != s2.month and s1.price != s2.price;

/* BCNF
Name : A | Discount: B
Month: C | Price   : D
R(ABCD): A -> D, C -> D, AC -> BD, CD -> AB, AB -> CD4

A+=AD, A+ != A, A+ != (ABCD)
THEREFORE: ABCD - AD => AD, ABC
R1(AD)

C+=BC, C+ != C, C+ != ABC
THEREFORE: ABC - CB => BC, AC
R2(BC), R3(AC)

R1(AD), R2(BC), R3(AC)
=> R1(Name, Price), R2(Discount, Month), R3(Name, Month)
*/

-- 4.3 & .4
CREATE TABLE NamePrice (
  name VARCHAR(100) PRIMARY KEY,
  price int
);
-- row number: 36

CREATE TABLE MonthlyDiscount(
  month VARCHAR(3) PRIMARY KEY,
  discount INT
);
-- row number: 12

CREATE TABLE NameMonth(
  name VARCHAR(100) REFERENCES NamePrice(name),
  month VARCHAR(3) REFERENCES MonthlyDiscount(month),
  PRIMARY KEY (name, month)
);
-- row number: 426
