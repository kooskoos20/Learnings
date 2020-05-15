Hierachy in SQL database

1. Materialzed path trees - 
	- Path attributes - A,AA,AB,AC,AAA
	- Strings get very long
	- Step size limits the size
	
2. Nested Set Models
	- Indexes - left and right integers
	- Add and delete difficult
	
3. Common Table Expression
	- AVL
	- Prone to error - left and right
	- Not much support - Use raw sql
	
4. Adjacent List
	- With CTE
	- w/o CTE
	
5. Closure Tables

Reference: 
https://media.ccc.de/v/hd-29-representing-hierarchies-in-relational-databases#t=1103
https://stackoverflow.com/questions/4048151/what-are-the-options-for-storing-hierarchical-data-in-a-relational-database
