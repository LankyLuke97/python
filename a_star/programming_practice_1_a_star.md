## Topic du Jour - the A* Pathfinding Algorithm

Over the last few months, I feel that I've become quite solid with various graph-based algorithms, whether it's the various search algorithms, Prim's, Kruskal's, or Kahn's. There's still plenty to learn - like Ford Fulkerson's maximum flow algorithm - but it seems to me that there's a glaring gap in the shape of an A. And an asterix. It's the A* algorithm, I can never remember the details.  

I've seen massive success with some types of study using flash cards, but this doesn't transfer quite as immediately to longer form, more complex items like implementing an algorithm. It can certainly help, if done correctly, but really the best approach is to do it yourself.  

## Doing it myself - the theory

Let's start with a few definitions so that I don't have to caveat the entirety of this piece. Although all of my work in this case was done on a grid, this can just as easily be considered a graph, where each node (or square) is connected to the nodes (or squares) around it. In my case, I have chosen to treat the nodes as being diagonally connected as well as along the cartesian grid. I am going to use the terms grid and graph interchangeably, as will I the terms node and square.  

In a graph, you connect nodes. If you don't, then you don't really have a graph. Ok, you still technically do, but I would question a) what use that graph is and b) your sanity.  

So, weights. I'm going to keep this simple for myself and treat the weights as an inherent characteristic of a node. That is to say, rather than assigning a weight to the trip from node A to node C and a different weight from node B to node C, I will instead say that node C has a weight that it costs to move to, regardless of which other node one is coming from. This doesn't have an effect on my understanding of the algorithm, but it does simplify some things for now.  

I started with just a basic implementation, without particularly focusing on performance. The core of the A* algorithm is a miniumum heap of some kind, tracking what's known as the f-score. The f-score is the weight, or distance, or time, or whatever flavour you have assigned to your graph, that it has so far cost to reach a given node, *plus the estimated cost from that node to your target node*. How do you estimate this, given that we probably wouldn't need the algorithm at all if we already knew the cost to reach our target from some arbitrary node? You need some sort of heuristic, or rule of thumb, that is *admissible* and, ideally though not strictly necessarily, *consistent*.  

It seems to me that the term *admissible heuristic* might be solely in use for this particular algorithm. It refers to a heuristic that never overestimates the actual cost of reaching the goal. That's it, pretty simple, though we'll come back to the implementation.  

A *consistent heuristic* is slightly more involved, but it essentially says that the heuristic for the cost to reach the goal from the current node must always be less than or equal to the cost to reach the goal from any neighbouring nodes once you include the cost of moving to that node. So, if I'm arbitrarily at node A, nieghbour of B, with an estimated cost to reach node C, __h(A)__, of 10 and a cost to move to node B, __AB__ of 3, then the heuristic must say that the cost to reach C from B, __h(B)__ is at *least* 7 - since then you have __h(B)__ + __AB__ <= __h(A)__. That makes sense to me, God knows how it will look when I read it back tomorrow.  

Back to the f-score. As stated above, there are two parts: the heuristic, and the current lowest score to reach the given node; this latter value is known as the g_score, and we'll track it with a dictionary (or map, or hash, or whatever your language of choice might term it). I could choose whatever value or function I like for the heuristic, provided it meets the criteria of admissibility. Since I know that the domain is a square-based grid and that all neighbours can be reached at all times, a reasonable heuristic is simply the Hamming distance from the current grid coordinate to the end goal.    

Ok, so we have our f-score. We store the f-score for each node in a min-heap, along with the node it's associated with. The algorithm then runs as follows:  
1. Pop the te with the minimum f-score from the heap.
2. For all neighbours of this node:
    1. Calculate a tenative g-score, which is the cost to travel from this node to the neighbour.
    2. Compare the tentative g-score to the stored g-score for that neighbour.
    3. If the tentative g-score is lower than the stored, update the backpointers dictionary for the neighbour to point to the current node, update the stored g-score for the neighbour to the tentative g-score, and add the neighbour, along with its freshly calculated f-score, to the min-heap.
3. Repeat until the goal is reached and the minimum-heap is not empty.  

That's it. Not all that difficult after all.  

The next thing I wanted to do was to visualise the path-finding in some way. Each year, I take part (badly) in Advent of Code, and I love seeing the visualisations that people come up with; I thought something similar here would be appropriate. I decided on a basic approach of writing a png file for each step of the algorithm; I used greyscale to represent the difficulty of moving into a grid square (normalising over the difficulties for all grid squares), with black being the easiest and white the hardest. Then, the current node being searched is coloured in blue, and all previously searched nodes are coloured red. Once the shortest path is found, a quick animation shows it clearly. The various png files are stored in a subfolder and compiled into a gif; if there are too many images to do so (because I didn't look into how to add more than a thousand files to a gif at which point the library and approach I'm using to do so start complaining about too many files), I switch to using **ffmpeg** to convert to an mp4. There's a lot to improve with this approach, but I just picked the thing that would get a visualistaion on screen the fastest.    

![Gif of A* algorithm](videos/path_shorter.gif)

![MP4 of A* algorithm](videos/path_larger.mp4)

(If you can't yet see the videos, I haven't got round to fixing the python code I'm using to convert from Markdown to HTML. At time of writing, it's converting the link to an img tag rather than a video tag.)

## Improvements

I would like to see what sort of performance gains I can get from this. First, though, I need to know the current performance, and for that, I'm going to use [Hyperfine](https://github.com/sharkdp/hyperfine). Without getting into the weeds, this is a neat little cli tool that automates the process of statistics gathering for a program. The output for the base performance (without writing to a gif or mp4, which is turned off for the remainder of this process), looks like this:  

![Base performance](images/programming_practice_1_1_perf_base.png)

What are some areas for improvement? The first place I am going to start is implementing what's known as the *tree-search* version of A\*, as opposed to the current *graph-search*. The difference is that the former uses a consistent heuristic and then dispenses with checking the tentative g-score with the previously stored g-score. Instead, if the g-score is stored at all, it must already be better than going from the current node.

So, the question is, do I have a consistent heuristic? As stated before, I'm using the Hamming distance from a node to the goal as the estimate. It's definitely admissible: each node costs *at least* 1...unit?...to move to, which is exactly what the Hamming distance measures. Is it, however, consistent? The way to check this, intuitively, is this: is the heuristic distance from node A directly to the goal node strictly less than or equal to the cost/distance stepping from A to another node B, plus the heuristic distance from node B to the goal? The answer to this, I think, is yes. Imagining a 2x2 grid, with node A in the upper left, node B in the upper right, and the node G in the bottom right, the heuristic from A to G would be 2, and the heuristic from B to G would be 1, with a minimum cost of moving to B of 1.  

So, we can remove steps 2.ii) and 2.iii) from the algorithm above, and simply add the node to the stored g-scores. To facilitate this, I'll move away from storing g-scores as a defaultdict and just use a dictionary, which will allow me to quickly check for existence of a neighbour within the dictionary, and skip the neighbour if it's already there. My reasoning as to why this will improve performance is that there defaultdict includes overhead, both in checking for existence and for using a lambda function, and that I remove another if check around the g_score comparison. The hyperfine results are as follows:  

![Tree search performance](images/programming_practice_1_2_perf_tree_search.png)

Wow - certainly a large improvement there. 64.5ms down from 111.6ms, that's a ~42% reduction in run time! What other tweaks can I make?  

I wanted to see if removing all the code around the visualisation would speed things up. At the moment, the visualisation is default disabled, and can be enabled with a command line option. The code that performs the visualisations is then wrapped in ```if``` blocks that check for this parameter; I wondered if this was causing overhead on each loop, so I deleted all the lines and ran the tuning again.  

![Removed visualisation checks](images/programming_practice_1_3_removed_visualisation_checks.ping)  

Almost no difference. Perhaps the interpreter does something smart to remove it, if it realises the boolean condition is always false? Or, maybe, there's just less overhead associated with it than I thought. I'll add the code back now.  

At this point, perhaps it's worth doing a bit of profiling to understand where the time is being spent. I ran the script via cProfile, with ```python -m cProfile -o a_star_profile.pstats a_star_demo.py```. This generates a file that I cannot read, but can peruse using pstats - or, alternatively, with snakeviz, that produces a lovely browser visualisation in the form of a flamegraph.  

![Flame chart of A* algorithm](programming_practice_1_4_flame_chart.png)

Something that stands out immediately is the Image module. I'm not using this when I'm not creating the visualisation, but it's still taking up...over half the run time?? Surely not. I could test that by just wrapping the import statements for the visualisation specific code in a single ```if``` check once the arguments have been parsed.

I'll leave this there for now. Further runs show very little time being spent in the search function. The rest of the time seems to be going on argparsing and loading modules, which is interesting to consider, but not what I want to investigate right now. Onto the next algorithm, I think.
