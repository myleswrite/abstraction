# abstraction

A Python script to work through a sitemap and see / save the meta descriptions. Really just a playground for me to learn a bit of Python at the moment.

## What does abstraction do?

+ Firstly it asks for the URL of a valid sitemap
+ Secondly it checks every URL in the sitemap and logs the meta description (if there is one)
+ Finally it (optionally) saves a JSON and CSV of the meta descriptions (not anymore, see below)

And that's it really. Like I said, it's just a way for me to learn a bit of Python.

## Version update

The new version (let's call it 2.0) now saves as a tab delimited file and asks for the file name at the start. This is so:

+ I don't use loads of memory building massive variables with the meta information for a single write at the end.
+ I don't need the JSON and CSV modules.
+ Tabs rather than commas so I don't have to worry about commas in the meta description / page title.

If you feel like buying me a beer for writing the script tip me here: <a href="https://www.paypal.me/mylesw42">https://www.paypal.me/mylesw42</a>
