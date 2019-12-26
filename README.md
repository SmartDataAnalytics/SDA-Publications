## SDA bibliography
Please follow the steps below in order to add your bib entries on sda bibliography.

* Fork the repository.
* Clone the forked repository.
    ```bash
    git clone https://github.com/YourGitHubAccount/SDA-Publications.git
    cd SDA-Publications
    ```
* Open sda.bib with [**JabRef**](http://www.jabref.org/) or a compatible editor and add your entries.

* Entries **must contain the *keywords* tag** and the entries must follow the guidelines described below.
    - The keywords are used to render a list of publications on the SDA website for each person, group and each project. In order for publications to show up in the correct lists, please pick a consistent keyword schema:
        * All _papers from one person_ should have a common keyword, for example the last name.
        * All _papers from one project_ should have a common keyword, such as the project name or an abbreviation thereof.
        * All _papers from one group_ should have a common keyword (e.g Distributed Semantic Analytics -> **DSA**, Semantic Question Answering -> **SQA**, Structured Machine Learning -> **SML**, Knowledge Graph Analysis -> **KGA**, Software Engineering for Data Science -> **SEEDS**, Semantic Data Management -> **SDM**)

* Entries should contain the *URL* tag with a free and direct PDF link (use a preprint version if the published one is not openly available).
* New entries should follow roughly the formatting of existing entries. If you add them with JabRef this will be taken care of automatically. Different versions of JabRef may produce a slightly different layout, but that is OK.
* Push your changes to your fork of the repository **after you are sure that *sda.bib* is still valid bibtex.**
    ```bash
    git add sda.bib
    git commit -m "Add paperX bib entry"
    git push
    ```
* Submit a pull request (PR).
