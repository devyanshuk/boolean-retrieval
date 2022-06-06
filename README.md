## Boolean Retrieval using Invertex Index



### Reasons for not using  Term-document incidence matrix.

While it's relatively easier to perform boolean retrieval using term-document incidence matrix - a 2-dimensional matrix of 1s and 0s, where the rows correspond to the ***unique terms(tokens)*** and the columns correspond to the ***documents***, and an entry ${x_{i}}_{j}$ corresponds to the presence/absence of a term in the document,

It can get absurdly large for large documents.

***As an example, from the 221 xml files, The total number of unique words and documents are as follows:***

| Title  | Total Number  |
|---|-----|
| Unique words | 24007001 |
| Total documents   | 81694   |

***

Before we compute the total size the matrix takes, we first find out the total size some data types in python take
```python3
>>> import sys
>>> sys.getsizeof("")
49
>>> sys.getsizeof("a")
50
>>> sys.getsizeof(1)
28
>>> sys.getsizeof(0)
24
>>> sys.getsizeof([random.choice([0, 1]) for _ in range(81694)])
711960
```
So, for a string of length n, the size in python would be $49 + len(n)$

### Assumption
1. Words are, on average, of length 6
2. Document ids are of length 14

| Title  | Total Size  |
|---|-----|
| Unique words | $24007001 * (49 + 6)$ bytes ~ $1.23 GB$ |
| Total documents   | $81694 * (49+14)$ bytes ~ $4.9 MB$   |
| Term-document matrix | $24007001 * 711960$ bytes ~ $15.5TB$  |

We do not account for the fact that python optimizes size for the matrix internally.
What we are interested in is that there are ~ $1.96 * 10^{12}$ elements in the matrix.

Due to this, as an optimization, we use the inverted index instead, where we disregard the 0 bits in the matrix.

This project utilizes the inverted index to store words to process queries for information retrieval.

***

### Representation

The inverted index, internally, is represented as a python-dictionary that maps ***words : string*** to ***collection of document ids : Hashset***

#### Example:
Note that these words may/may not be present in the dataset. It is just for illustration purposes.

| Word  | Document-Id  |
|---|-----|
| Sněžení | LN-20020105001, LN-20020105025 |
| World   | LN-20020105026  |
| hi | LN-20020105029  |

In this case, the inverted index would have the following structure:
```python3
{
	"Sněžení" : Hashset([ "LN-20020105001", "LN-20020105025" ]),
	"World"   : Hashset([ "LN-20020105026" ]),
	"hi"      : Hashset([ "LN-20020105029" ])
}
```
Storing the document-ids in a hash-set would make it very fast to access (O(1) on average)

# Query Evaluation

All 25 queries from documents_cs.xml file are processed one-by-one and then the output is stored to a file name inside num tag.

### Example:

***Sněžení OR World***

1) Convert the query to a list of query tokens. ["Sněžení", "OR", "World"]
2) Convert the list to a postfix representation. ["Sněžení", "World", "OR"]
3) Evaluate the postfix:

| Postfix list  | Stack  |
|---|-----|
| ```["Sněžení", "World", "OR"] ``` | ```[] ``` |
| ```["World", "OR"] ```  | ```[ Hashset([ "LN-20020105001", "LN-20020105025" ])  ]```  |
| ```["OR"] ```  |  ```[ Hashset([ "LN-20020105001", "LN-20020105025" ]), Hashset([ "LN-20020105026" ])]``` |
| ```[] ``` | ```Hashset([ "LN-20020105001", "LN-20020105025",  "LN-20020105026" ]) ``` |

In the last step, the QueryProcessor performs the union operation on the two Hashsets.


# Hashset

A hashset is used instead of the already-present python lists, for faster document-id storage, and also for faster query operator evaluation.

The hashset I used uses a **32-bit modular hash** to store elements in the bucket.
If two items have the same hash, I use a linked-list to store elements with the same hash.

##### Some methods in the Hashset class vital for the query evaluation

### UNION [ O(|hashset_b|) ]

Elements of hashset_a or hashset_b

```python3
union(Hashset hashset_a, Hashset hashset_b):
	new_hashset = hashset_a
	for element in hashset_b:
		if element is not present in new_hashset then
			store element in new_hashset
```


### INTERSECTION [ O(|hashset_a| + |hashset_b|) ]

Elements that are present in both hashset_a and hashset_b
```python3
intersection(Hashset hashset_a, Hashset hashset_b):
	new_hashset = Hashset()
	for elment in hashset_a:
		if element is present in hashset_b then:
			store element to new_hashset

	for element in hashset_b:
		if element is present in hashset_a then:
			store element to new_hashset
```

### AND-NOT [ O(|hashset_a|) ]

Elements of hashset_a that are not present in hashset_b

```python3
and_not(Hashset hashset_a, Hashset hashset_b):
	new_hashset = Hashset()
	for element in hashset_a:
		if element is not present in hashset_b then:
			store element in new_hashset
```

## Project Structure

Before running the program, make sure that the dataset (***A2/ is in the same directory the main.py file is in***).

***If not, refer to step (2) of the running guide below.***

```python3
BOOLEAN-RETRIEVAL
│   README.md
│   requirements.txt
|	README.pdf
|	Makefile
│   main.py
│
└───A2/
│   │   queries_cs.xml
│   │
│   └───documents_cs/
│       	│   czech.dtd
│       	│   ln020101.xml
│       	│   ...
│   
└───bin/10.2452/
|   	│   401-AH
|   	│   402-AH
|		│   ...
|    
|    
|___invertexindex/
|	 	|	__init__.py
|    	|	indexer.py
|    	|
|    	|___map/
|    	 	|	__init__.py
|    	 	|	hashset.py
|    	 	|	node.py
|    	 	|	...
|    
|    
|____iohandler/    
     	|	__init__.py
     	|	helpers.py
     	|	queryprocessor.py
     	|	reader.py
     	|	...

```

## Running the Program

### Setting up  a virtual environment
```
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```


1. ***Store all words from the 221 xml files, evaluate queries from queries_cs.xml and store results to files (verbose flag enabled)***
      ```
      (venv)$ make all
      ```
	&emsp;&emsp; __OR__

      ```
      (venv)$ python3 main.py --verbose
      ```

2. ***Specify the base directory the dataset is in (A2/ by default)***
      ```
      (venv)$ python3 main.py --verbose --data_path=A2/
      ```

3. ***Store all words and evaluate queries, but without being verbose***
      ```
      (venv)$ python3 main.py
      ```

4. ***Save the stored words as a pickle file for future use (evaluates the queries too)***
      ```
      (venv)$ python3 main.py --verbose --save
      ```

5. ***Remove all project-generated files and directories***
    ```
    (venv)$ make clean
    ```
