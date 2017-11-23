# Readme 

This is the github repo of Stanford's Causality in Cognition Lab homepage.  

## Basic organization 

- `content`: contains markdown files used to render the page 
   + `home`: all widgets displayed on the first page 
   + `member`: individual markdown file for each lab member 
   + `publication`: individual file for each publication 

- `static`: contains all the files (papers, images, datasets, ...) in several subfolders

## Update the hompage 

If you have any trouble getting things to work, feel free to post an issue on the github repo. 

To submit any changes you've made, navigate to the root directory of the homepage in your terminal and run:

```
bash publish.sh 'message'
```

Please type a 'message' that communicates what changes you've made. 

### Add yourself to the homepage

#### Add your picture

- Make sure that the image is not too large. 
- Ideally, it should be square. 
- Name the picture `firstname_lastname.jpg` and put it into `static/img/members/`. 

#### Add your CV 

- Name your CV `firstname_lastname.pdf` and put it in `static/cv/`.

#### Add your personal page 

You can create a new webpage by adding a new markdown file with your name into the `content/member/` folder. Just copy the `tobias_gerstenberg.md` file, rename it, and adapt it to your needs. 

#### Update the people page 

In `content/home/people.md` add yourself as a new member. You can simply copy the template. If you don't have twitter or any of the other services, just leave it empty (e.g. `twitter = ""`). 

### Add a publication 

#### Update the lab's bibtex file 

- The lab's bibtex file is located here: `static/bibtex/cic_papers.bib`. 
- Add the bibtex entry of your publication to the file. 
- Make sure to add an abstract to your entry. 

#### Parse the bibtex file to update the homepage

In your terminal, navigate to the root folder and run: 

```
python3 parse_bib_cic.py -i static/bibtex/cic_papers.bib
```

This will create a new markdown file in the `content/publication/` folder for each new publication that was added to the lab's bibdesk repository. The markdown file is named `bibentryid.md`, for example `gerstenberg2016csm.md`. 

The parser also puts individual `.bib` files for each publication into `static/files/citations/`. 

#### Add a pdf of your paper 

Add a pdf of your paper to `static/papers/` using the same name as the markdown file above (e.g. `gerstenberg2016csm.pdf`).

#### Tweak the publication page 

Navigate to `content/publication/` to open the publication. Adapt the links: 

```
# Links (optional).
url_pdf = "papers/gerstenberg2016csm.pdf"
url_preprint = ""
url_code = ""
url_dataset = ""
url_project = ""
url_slides = "https://link_to_slides.pdf"
url_video = ""
url_poster = ""
url_source = ""
```

You can also generate new links by changing `url_custom = []` to 

```
url_custom = [
{name = "link_name1", url = "url1"},
{name = "link_name2", url = "url2"}
]
```

You can also add an image to go with the paper by putting it into `static/img/publications/` and linking to by adapting the `image =""` parameter (e.g. `image ="publications/gerstenberg2016csm.png"`).

## Tutorial links 

- https://georgecushen.com/create-your-website-with-hugo/