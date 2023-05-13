Title: Using Python, Pelican, and PyCharm as my publishing tools  
Date: 2023-05-13 12:00  
status: draft  

## Summary  

I use Markdown, Pelican, PyCharm, git and GitHub in my web publishing tool chain.

## Introduction  

In The Old Days, one might edit html files on a simple text editor, 
ftp them to a host site, and then view the rendered results. 
You can still do that if you really want to. 
One did not need to be concerned with nuances such as CSS and 
SSL certificates. 

There are now many other options. 
Below is the tool chain that I have adopted for blogging. 

I have modest requirements. 
My blog gets a few hundred hits a week, sometimes a few thousand. 
I do not need interactive features like sign-ups or comments
(I get feed back through other social media). 
I am not interested in SEO (search engine optimization). 
I do not want to track users and set cookies. 
I do not want advertisements on my site. 
Also, I do not plan to monetize my blog. 
If I had different needs, I might have made other choices. 

## [Markdown](https://daringfireball.net/projects/markdown/)  

Posts are written in the Markdown syntax. 
This saves me from having to deal with raw HTML. 
The posts are also easily human-readable in the Markdown format
(where html is barely readable). 
Included is a Markdown table formatter that I find useful. 

As an example, the header above in Markdown:  
```markdown
## [Markdown](https://daringfireball.net/projects/markdown/)
```

This gets processed by Pelican (see below) as html:  
```html
<h2><a href="https://daringfireball.net/projects/markdown/">Markdown</a></h2>
```

## Pelican  

I use the pelican static website generator.  
[blog.getpelican.com](https://blog.getpelican.com/)  

I selected it partly because it is written in python, and I was already familiar with python. 
In addition to processing Markdown as shown above, 
it integrates the separate webpages in to a navigable whole. 

Static sites offer many advantages. They are written mainly in HTML, with some CSS styling. 
This enables many low or no cost hosting options. 
However, they do not offer interactive features such as sign-ups and comments. 

### Metadata  

In addition to the Markdown content, a file has metadata that 
helps Pelican generate the website navigation. 

"Title:" gives the post a filename.html 
(indirectly, as the "Title:" gets sluggified to the filename). 
Optionally, you can define the slug directly, such as "Slug: my-super-post". 
Note that the slug must be unique, or you will get errors when the static site is built. 

A "Date:" is the publishing date. 
There are also "Tags:", 
and a "Status:". 
A post starts with "Status: draft", and that is changed to 
"Status: published" when a post is ready to publish 
(or delete the status line, depending on publishconf.py settings).  

### <a name="site-navigation"></a> Site navigation  

Pelican assumes that you want a chronological blog. 
I have added pages that provide navigation other than chronological 
[Site Navigation and Suggested Reading Order](https://icinganalysis.com/site-navigation-and-suggested-reading-order.html). 
I also set my introduction page to be index.html (save_as: index.html), 
otherwise pelican defaults to the generated blog.html.  

I set the menu items in the publishconf.py file:  
```python
MENUITEMS = (
    ('Home', '/index.html'),
    ('Suggested Reading Order', '/site-navigation-and-suggested-reading-order.html'),
    ('Latest Posts', '/archives.html'),
    ('About', '/about.html'),
)
```

Some flavors of Markdown let you use headers as internal link anchors

```markdown
### Metadata  

[link to Metadata](#metadata)
```
> [link to Metadata](#metadata)  

But with the flavor of Markdown that comes with Pelican, one needs to put an anchor in the header:  
```markdown
### <a name="site-navigation"></a> Site navigation

[link to Site Navigation](#site-navigation)
```
> [link to Site Navigation](#site-navigation)  

Anchor links also work between pages:  
```markdown
[Conclusions of Icing on Cylinders Drop Size Distributions]({filename}cylinder_thread_wrap_up.md#drop_size_distributions)
```
> [Conclusions of Icing on Cylinders Drop Size Distributions]({filename}cylinder_thread_wrap_up.md#drop_size_distributions)  

## PyCharm 

[jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/)  

I use the PyCharm IDE (interactive development environment) as a markdown editor, 
as an interface to git, and for pushing to GitHub. 
I was already familiar with the PyCharm editor and git, 
which made the transitions to blog editing easier. 
If I was not already familiar, I might have made another choice. 

Here are some nuances and limitations I have noticed. 

### Markdown in PyCharm  

There is support for Markdown files and editing. 
A preview of the rendered page is available. 

However, there are several flavors of Markdown, and the flavor used for the 
preview is slightly different from the flavor used by Pelican, 
the static site generator that I use. 
Pelican can provide a local server, so you can see what the rendered files in 
a browser window. The preview and the browser view may not be identical. 

### Pelican path considerations  

Pelican generally integrates well PyCharm, but there are some considerations. 

To create a link to another page of the website, one includes 
{filename} in the path: 

```markdown
[Welcome]({filename}introduction.md)  
```
> [Welcome]({filename}introduction.md)  

This allows Pelican to resolve the path, whether the 
page has "status: draft" or otherwise. 

PyCharm attempts to create links for internal pages by simply 
copying the filename2.md from the "Project" view, and pasting 
it in filename1.md. However, it does not include the {filename} 
part, and I have made many publishing errors due to this. 

One advantage of the copy-and-paste method is that PyCharm converts 
characters to a web-portable format. Characters such as space " " 
get converted to "%20". For GitHub Pages hosting (see below) the 
portable format has not been an issue, 
but it might be for other hosting options. 

### Images and drafts  

Drafts are valuable to see what a post will look like before it is published. 
Either python or Pelican can provide a local server. 
Pelican save pages with "status: draft" in a /docs/drafts folder. 

One nuance for viewing draft posts is how the path to images is defined. 
```text
![airplane_banner_colorized](images%2Fairplane_banner_colorized.png)
```

![airplane_banner_colorized](images%2Fairplane_banner_colorized.png)

```text
![airplane_banner_colorized2](/images%2Fairplane_banner_colorized.png)
```

![airplane_banner_colorized2](/images%2Fairplane_banner_colorized.png)

Depending on how the post is viewed, an initial '/' affects whether the 
image is reachable:  

| Production posts         | images | /images |
|--------------------------|--------|---------|
| Production server from / | yes    | yes     |

| Draft posts                    | images | /images |
|--------------------------------|--------|---------|
| Production server from /drafts | no     | yes     |
| local server                   | no     | yes     |
| PyCharm preview                | yes    | no      |

I generally do not verify images in the preview. 
Sometimes, I do take a peak in the PyCharm preview by temporarily adding /images, 
but this is not a "best practice", as it does not work for drafts on the production server, 
and I have often forgotten to change it back. 

## Git   

PyCharm also includes integration with git, 
with git commands available as quick key combinations, 
such as ctrl-k for commit, and shift-ctrl-k for push. 

## Working with GitHub  

GitHub serves several functions. 
It is a central repository that allows one to freely share code. 
It also provides a server for static websites, 
[GitHub pages](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages), 
such as this one [icinganalysis.github.io](https://icinganalysis.github.io). 
It also integrates well with other website servers, such as the mirror site 
[icinganalysis.com](https://icinganalysis.com/). 

The GitHub Pages service provides several details, 
such as a default URL (icinganalysis.github.io), 
and an SSL certificate for https service. 

Once credentials are set up, one can push to GitHub with ctrl-shift-k. 
Website changes are usually visibly to the world within about four minutes. 

GitHub can also process Markdown format files using [Jekyll](https://jekyllrb.com/). 
However, I have turned that off by placing a .nojekyll file in the directory. 

While I have not used it, GitHub Pages offers an option to use a custom URL
(see "Why have a mirror site?" below).  
 
Neither the local server nor the PyCharm preview can check if a file 
is properly pushed to GitHub 
(although PyCharm issues a notice if a push fails, 
it does not check the path considerations noted above). 
So, be sure to check the production server view. 

It is not uncommon (about 25% of the time) that when I push changes to 
GitHub that I get an error message such as:  
> [icinganalysis/icinganalysis.github.io] Run cancelled: pages build and deployment - gh-pages  

There is usually no fault that I can find in my files, 
so it appears to be GitHub load related (the free tier of service may not get prioritized). 
I can manually re-run the deployment from my GitHub account, and the website updates properly. 

## Why have a mirror site?  

As GitHub has a no-cost tier of service, one may wonder why a mirror site is desirable.  

One reason is to have a custom URL (although GitHub Pages offers an option to use one), 
[icinganalysis.com](https://icinganalysis.com/), 
which is stable if I choose to change the hosting site. 

Another is that while GitHub currently has a no-cost account level that meet my needs, 
that may not continue forever. 
By having a mirror site, I have already worked out how to host a site elsewhere, 
and can easily react to changes.  

I selected [DigitalOcean](https://cloud.digitalocean.com/login) as the host. 
DigitalOcean also provides the SSL certificate. 
I partly chose it because I was already familiar with it. 
However, there are many other, comparable hosts sites. 
I "own" the URL (not really, one rents one with yearly renewal fees), 
so I can host it wherever is convenient. 
