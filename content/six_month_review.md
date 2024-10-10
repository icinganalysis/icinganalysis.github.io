title: Six Month Review of Blast from the Past: NACA Icing Publications    
Date: 2022-07-13 12:00  

### _"You can't connect the dots looking forward; you can only connect them looking backwards."_ 
_Attributed to Steve Jobs._  

![Figure 8 of NACA-TN-339. Test on glucose coating. Heavy spray. Temperature -1 degree C.
Air speed 70 mph.](images/naca-tn-339/Figure 8.png)  
_One of the earliest icing wind tunnel tests on surface coatings to prevent ice, NACA-TN-339, 1929. Sometimes, there is a learning curve._  

## Summary

I have been posting for about six months now, 
so it is time to review how it is going.  

I thank all of my readers. 
I want to write things that are read, and you make this worthwhile. 

I started out with the statement ["I make selected NACA publications easily accessible to you"]({filename}introduction.md). 
By some measures, I have been achieving that, 
and I welcome your opinions of how well I am doing. 

## Discussion  

## Things that work

### Interest in the topic  

I presented ["NACA Publications on Aircraft Icing: Cylinders"](https://icinganalysis.github.io/images/cylinder_thread_wrap_up/SAE%20presentation%20Cook.pdf) 
to the SAE AC-9C Aircraft Icing Technology Committee and it was well received. 

A measure of interest is views of a post. 
My average post gets about 300 views, 
which exceeds what I thought it would be (a few dozen, perhaps). 

One post went "viral", by my modest standards, with 4000+ views (and still adds a few now and then), 
[Messinger, B. L.: Equilibrium Temperature of an Unheated Icing Surface as a Function of Airspeed]({filename}messinger.md). 
I suppose it is a well known title in aircraft icing, 
and people want to see it summarized. 

### LinkedIn

I usually post a link to the latest post on my website on LinkedIn. 
I thought that LinkedIn would be just one of several ways of getting my posts noticed, 
but it has turned out to be the main avenue. 

I think that having been already connected with several people 
with interest in the topic on LinkedIn when I started helped get things going.
My number of connections and followers has grown. 
The typical views of a post now exceed my number of connections and followers. 

While I do not use cookies and tracking on my website, 
LinkedIn tracks the posts that I make there. 
It provides information on "impressions" (how many screens a post rolls by on, I guess) 
and people "reached" (how many people actually click on an article, I guess).
The "reached" is about 60% of the "impressions" for my posts. 
I assume that an interesting quote and image at the top of the LinkedIn post help 
people to want to click through and read further. 

I am not sure how to quantify things such as the "like" emojis, 
but each post typically gets some (and thank you for the likes). 

I am not sure how much the hash tags (typically #icinganalysis and #aircrafticing) 
contribute to views. 

### Git and Github

I am glad that I used a file tracking system from the start. 
I used git (although there are others). 
It definitely helps me keep track of things
(and things are getting complex, with 50+ posts and hundreds of images). 
It lets me fearlessly revise things while editing 
(a kind of global "undo" button, as long as I "commit" every so often). 
Note that both the web content and the python files are under git. 

When a computer drive on my laptop crashed, 
I was quickly able to get back to writing, 
as there was a complete copy on GitHub.

The python executable files are available under LGPL license at [icinganalysis.github.io](https://github.com/icinganalysis/icinganalysis.github.io/tree/main/icinganalysis) 

Github also works as the web server. 
The no-cost tier of service works for me (a website with static HTML files), 
but if things change the HTML and image files are easy to 
re-host somewhere else. 
I do have a domain name, icinganalysis.com, 
which currently re-directs to icinganalysis.github.io, 
so I could start using that as the main link. 

## Things that sort-of work

### Progress on the 131 Historic NACA Icing Publications 

To date, I have posted 56 reviews, but only 26 of the from the ["Selected Bibilography of NACA-NASA Aircraft Icing Publications"]({filename}/The Historical Selected Bibliography of NACA-NASA Icing Publications.md).  
That puts me on a three-year trajectory to review them all. 
(I am not sure that I will get there.) 

I my defense, the other reviews were pertinent topics, 
and some of them generated much interest 
(such as [Messinger, B. L.: Equilibrium Temperature of an Unheated Icing Surface as a Function of Airspeed]({filename}messinger.md), 
[NACA-TN-313, "The Formation of Ice upon Airplanes in Flight"]({filename}NACA-TN-313.md), 
and [Irving Langmuir, "Super-Cooled Water Droplets in Rising Currents of Cold Saturated Air"]({filename}Langmuir Rising Currents.md) 
the three most popular posts, each with over 1000 views). 

### Searchability

Searchability is part of accessibility. 
If someone cannot find the information, it is not very useful. 

When I search "Selected bibliography of NACA-NASA aircraft icing publications" on two search engines
(duckduckgo.com and google.com), my web page ["Selected Bibilography of NACA-NASA Aircraft Icing Publications"]({filename}/The Historical Selected Bibliography of NACA-NASA Icing Publications.md) 
shows up on the first page 
(your experience may be different, as search engines may tailor results to users). 
This was one of my goals, to make this readily available in a legible form, 
and machine-readable (if you count HTML).

However, if I search "NACA-TN-1904", my review at [NACA-TN-1904 "Observations of Icing Conditions Encountered in Flight During 1948"]({filename}/NACA-TN-1904.md) 
shows on the first page of duckduckgo.com, but on google.com 
only my twitter post (which never got traction) about it shows up
(the review might be somewhere in the google results, many pages down).

I don't know much about search engine optimization, 
and I don't want to add a lot of junk to the web pages to try and boost it. 

###My web tools

You can see my tools listed at [Web publishing tools]({filename}web publishing tools.md).  

Pelican and markdown have a learning curve. 
One of these days I might get Latex equations working. 
The pelican CSS theme "notmyidea" is not perfect for my application, 
but it works with mobile displays, and I don't 
want to spend my time perfecting CSS. 

I have grown quite comfortable with the markdown format for writing. 
The limitations are actually liberating, not getting bogged down into too many options. 
Markdown also allows one to include HTML if needed. 
I have found that I prefer things like two simple markdown tables, 
rather than one complex HTML table with merged cells, 
both for writing and the final product. 

I have tried other tools stacks for other websites, 
and this is the one that has worked best for me
(they all have advantages and challenges). 

## Things that have not worked (yet)

### Interest in the python code files

Github tracks how often a repository is cloned, 
and [mine](https://github.com/icinganalysis/icinganalysis.github.io/tree/main/icinganalysis) has been cloned a few times. 
There have been no forks. 

I put a poll on LinkedIn asking if people have used the code, 
and so far no one has voted that they have used the code. 

The post [Python programming style guide]({filename}python_style_guide.md)  
received over 300 views, 
so there appears to be interest in python in general. 

As an experiment, I stopped placing executable code in the repository in May, 
and no one noticed 
(or at least no one complained). 

Oh well, I hold out hope that there will be more interest when 
we get to icing wind tunnel test similarity. 

### Other media and feedback

I made a separate email account for icinganalysis, and no one has commented through that. 

I posted for a while on Twitter, and got no feedback. 

I have had some activity on researchgate.net, 
mostly from authors who are kindly willing to share their papers. 

There have been some kind text comments on LinkedIn, but not many comments of any sort. 

## Conclusion

Again, I thank my readers. 

I plan to continue posting.

For the upcoming [Icing Wind Tunnels Test Thread]({filename}Icing Wind Tunnel Test Thread.md) 
I will be trying something a little different, 
grouping several publications into a single topic review, 
and including more post NACA-era information. 
This may accelerate getting through the publications, 
but as I said above, I may not get through all 131 NACA icing publications. 

I welcome feedback about what will most useful to you in future posts. 





