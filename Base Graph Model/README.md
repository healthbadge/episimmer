
To run model : python Main.py config.txt <graph flat file>



Config file format(.txt):

    Number of worlds : 30
  
    Number of Days : 30
  
    Starting Exposed Percentage : 0.3
  
    Starting Infected Percentage : 0



Graph Flat file format(.txt):

 Currently there are two formats. Code to generate them is given in folder Generate Graph.
 
      -Simple Adjacency List (txt file)
       first line contains number of nodes(n) indexed from 0 to n-1
       every subsequent line contains the node followed by it's adjacency list all separated by spaces
      
      
      -Simple Edge List (txt file)
      first line contains number of nodes(n) indexed from 0 to n-1
      every subsequent line represents an directed edge(s->t) and contains two vertices(s t) separated by a space
