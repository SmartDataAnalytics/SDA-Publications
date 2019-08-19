## SDA bibliography
Please follow the steps below in order to add your bib entries on sda bibliography.

* Fork the repository
* Clone a forked repository
    ```bash
    git clone https://github.com/YourGitHubAccount/SDA-Publications.git
    cd SDA-Publications
    ```
* Open sda.bib with [**JabRef**](http://www.jabref.org/) or a compatible editor and add your entries.
* Entries must contain the keyword tag, which must contain your publication tag (see http://sda.cs.uni-bonn.de/people/prof-dr-jens-lehmann/ - publications). The tag included in the Keywords could be per-person (e.g `lehmann`), per-project (e.g `sansa`: http://sda.cs.uni-bonn.de/projects/sansa-stack/), per-group (e.g. `dsa`: http://sda.cs.uni-bonn.de/research-topic/distributed-semantic-analytics/)
Entries should contain the URL tag with a free and direct PDF link (use a preprint version if the published one is not openly available).
* Push your changes in your fork of the repository
    ```bash
    git add sda.bib
    git commit -m "Add paperX bib entry"
    git push
    ```  
    <sub>After you are sure that __sda.bib__ is still valid bibtex.</sub>
* Submit a pull request (PR).

