These scripts worked for me. There's no guarantee they will work for you.

Octopress 2 Ghost
---

A python script to process Octopress markdown files and write a JSON file ready to import into Ghost.

These are the preliminar steps:

* Setup Ghost, signup, signin and remove the welcome post.
* Go to `/ghost/debug` and export the database. It'll save a file named `GhostData.json`.
* Download `octopress2ghost.py` and install the requirements: `pip install translitcodec`

Run the conversion script:

`python octopress2ghost.py <octopress-posts> <ghost-data> | python -mjson.tool > import-this.json`

Where octopress-posts is a directory with the Octopress posts and ghost-data is the JSON exported from Ghost.

Now go to `/ghost/debug` and import the obtained JSON file.

If everything goes well you should be able to signin again and all your Octopress posts will be there.

Octopress HTML 2 Markdown
---

A python script to generate Octopress markdown files from published HTML files.

Specify:

* Octopress directory
* Published blog directory
* Generate a list of absolute paths of all the published HTML files using command line utilities and
  save the list to a file
