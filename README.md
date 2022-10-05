My code is simple to run you can just execute run.sh
run.sh does depend on a jgraph executable to present in the current directory


Understanding the graphs:

Just a preface this is slightly boring on an idle machine, so I suggest running things while run.sh is running to see more results

First the graph with user, system, and nice times (along with total idle otherwise).
This graph is quite simply the comparison of those things in a nice graphical form
The colors are supposed to replicate htop's denotion of these CPU usage stats

Next is the graph below which is total CPU usage
This graph could vary from the graph above, because it takes little things into account that I do not
I.E. virtual time, IRQ time, IO wait time, guest time, and steal time
But it should paint a nice picture between analyzing the two of them
I could have included those times in the first graph, but thought against it since I though the 3 I chose were sufficent

The last graph is an interesting one
I shows total cpu usage and memory usage since the program start
It takes the top 10 most heavy CPU reliant processes
I know there is duplicates of processes, those extra instances (or children)
If I spent more time I could've added the name of the instance (or child) but I really just wanted something I could glance at
and understand what was taking lots of CPU or memory!

If you have any trouble please reach out

It came to my attention after testing on different machines that the jpeg output seems to be cropped weird. I can add some pictures on my end.
