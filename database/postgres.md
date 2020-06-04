json data can be stored in relational databases using jsonb

The data types json and jsonb, as defined by the PostgreSQL documentation,are almost identical; the key difference is that json data is stored as an exact copy of the JSON input text, whereas jsonb stores data in a decomposed binary form; that is, not as an ASCII/UTF-8 string, but as binary code.

```
CREATE TABLE books (  
  book_id serial NOT NULL,
  data jsonb
);
```

Potgres

1. fill factor

The fillfactor for a table is a percentage between 10 and 100. 100 (complete packing) is the default. When a smaller fillfactor is specified, INSERT operations pack table pages only to the indicated percentage; the remaining space on each page is reserved for updating rows on that page. This gives UPDATE a chance to place the updated copy of a row on the same page as the original, which is more efficient than placing it on a different page. For a table whose entries are never updated, complete packing is the best choice, but in heavily updated tables smaller fillfactors are appropriate.

2. A database contains one or more named schemas, which in turn contain tables. Schemas also contain other kinds of named objects, including data types, functions, and operators. The same object name can be used in different schemas without conflict; for example, both schema1 and myschema can contain tables named mytable. Unlike databases, schemas are not rigidly separated: a user can access objects in any of the schemas in the database he is connected to, if he has privileges to do so.

There are several reasons why one might want to use schemas:

To allow many users to use one database without interfering with each other.

To organize database objects into logical groups to make them more manageable.

Third-party applications can be put into separate schemas so they do not collide with the names of other objects.

Schemas are analogous to directories at the operating system level, except that schemas cannot be nested.
