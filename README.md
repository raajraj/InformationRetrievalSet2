# CS172 - Assignment 2 (Retrieval)

## Team member 1 - Raajitha Rajkumar 862015848
## Team member 2 - Russell Brown 862024798

## DESIGN

#### For this assignment, we build off of assignment #1, and create an output folder with format
<query−number> Q0 <docno> <rank> <score> Exp
#### We implemented this code by writing a VSM.py file that takes in an argument for a file and reads in the file omitting the first number. We first normalize all the words in the query and find the query term frequency for each term. We also call parsing.py from our pervious assignment to get the term frequency for each document for each word in the query and get the DF for each word. We can cross multiply those values and get a list off all TF:IDFS needed for the cosine similarity. We then compute the cosine similarity of all documents to the query, sort them, and rank the top 10 for their similarity.

## HOW TO COMPILE

### To run this assignment is simple, but can only be done a specific way. First, pick a file with the query format that is provided or one on your own. In this case the format is query_list.txt. Then write the file you want the output to go to. Here are some examples

```python
$ python3 VSM.py query_list.txt > output.txt
```
```python
$ python3 VSM.py query_list.txt > output2.txt
```
### Anything that is not in that format will result in an error. A term or document that does not exist will also result in an error. We submitted an output file called output.txt to demonstrate what it should look like. 
