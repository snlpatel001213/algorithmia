Selective Search uses Graph search to find so called "Initial regions" as proposed in [1].

Efficient Graph-Based Image Segmentation treats each image a graph with each pixel in the image as Vertices and distance between two pixel as weight of edge.
to calculate distance between two pixel(vertices), one can use simple measure such Euclidean distance.

As per [2] The method to calculate graph from image can be formally defined as as : 
We assume that an image is given as a p x q array
and each pixel has an integral gray level E [0,.X],
i.e. the whole gray scale [0, l] is divided and discretized
into X + 1 gray levels. For a given 2D gray-level image
I, we define a weighted planar graph G(Z) = (V,E),
where the vertex set V = {all pixels of I} and the edge
set E = {(u, ZJ)]U, w E V and distunce(u, TJ) 5 a}, where
distunce(u, w) is the Euclidean distance in terms of
the number of pixels; each edge (u, V) E E has a weight
W(U, V) = IQ(u) - B(V)], with B(X) E [0, X] representing
the gray level of a pixel x E I. Note that G(Z) is a connected
graph, i.e. there exists a path between any pair of
vertices, and any vertex of G(Z) has at most 8 neighbors. 

Well Well Well... this is bit complicated, lets simplify a lot. 
1) Lets say we have an image X. Generally image have 3 channels and it is made up of pixels as shown in image below.
2) Lets consider all pixels as all vertices of the graph.
3) calculate distance between all adjacent vertices in directed manner. For that, start form upper left corner of the image
and continue to the lower right corner of the image. While traversing in this manner you can calculate distance 
between selected pixel and other three pixels \[1) Pixel right to selected one, 2)Pixel bottom to selected one, and 3) Pixel diagonally bottom-right to selected one\]. 
This all distances will create a weighted uni-directed graph.Note that grapg so created is a connected graph, i.e. there exists a path between any pair of
vertices, and any vertex of graph has at most 8 neighbors.

We are done with creating graph, next we require a minimum spanning tree of this graph. Minimum spanning tree can be described as. 
>A minimum spanning tree (MST) or minimum weight spanning tree is a subset of the edges of a connected, edge-weighted (un)directed graph that connects all the vertices together, without any cycles and with the minimum possible total edge weight. 

Minimum spanning tree simplifies the graph and provide that path between pixel which are connected by minimum distnace. It may 
seem confusing at this point of time but you will get clear picture soon. I applied algorithm to get minimum spanning tree and I got following picture. 

Original Picture 

I applied various threshold and all picture are as follows:


It is clearly visible that background and foreground are perfectly separated at some threshold level. 
This is what it looks like after applying MST. 
Now in order to segement different region we require to break this tree in ti different parts based on 
difference in weights. Selective search uses specific method called "Hierarchical Grouping Algorithm" to do this. In "selective search" paper it is given as follow:

Hierarchical Grouping Algorithm
Input: (colour) image
Output: Set of object location hypotheses L
Obtain initial regions R = {r1,··· ,rn} using [1]
Initialise similarity set S = /0
foreach Neighbouring region pair (ri
,rj) do
Calculate similarity s(ri
,rj)
S = S∪s(ri
,rj)
while S 6= /0 do
Get highest similarity s(ri
,rj) = max(S)
Merge corresponding regions rt = ri ∪rj
Remove similarities regarding ri
: S = S \ s(ri
,r∗)
Remove similarities regarding rj
: S = S \ s(r∗,rj)
Calculate similarity set St between rt and its neighbours
S = S∪St
R = R∪rt
Extract object location boxes L from all regions in R

Lets simplify this algorithm with following step:
1)  We have already generated 
 
 
[1] Efficient Graph-Based Image Segmentation | https://www.cs.cornell.edu/~dph/papers/seg-ijcv.pdf 
[2] 2D image segmentation using minimum spanning trees | https://doi.org/10.1016/S0262-8856(96)01105-5
