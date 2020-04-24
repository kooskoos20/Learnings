json data can be stored in relational databases using jsonb

The data types json and jsonb, as defined by the PostgreSQL documentation,are almost identical; the key difference is that json data is stored as an exact copy of the JSON input text, whereas jsonb stores data in a decomposed binary form; that is, not as an ASCII/UTF-8 string, but as binary code.

```
CREATE TABLE books (  
  book_id serial NOT NULL,
  data jsonb
);
```
