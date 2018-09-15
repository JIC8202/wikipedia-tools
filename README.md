# wikipedia-tools
scripts for analyzing wikipedia dumps

## Usage
### link finder
```
linker.py [-h] page_links pages_from pages_to output
```
where:
* `page_links` is the pagelinks database from [wikipedia dumps](https://dumps.wikimedia.org/backup-index.html), converted into CSV format
* `pages_from` is the output of a [PetScan](https://petscan.wmflabs.org/) query in JSON format, representing the pages to use as link sources
* `pages_to` has the same format as `pages_from`, but corresponds to to link targets
* `output` denotes the output file, saved as a list of nodes and edges in JSON format

### mysqldump-to-csv converter
see [jamesmishra/mysqldump-to-csv](https://github.com/jamesmishra/mysqldump-to-csv)

## Example PetScan queries
* [Science fiction writers](https://petscan.wmflabs.org/?language=en&project=wikipedia&depth=10&categories=Science%20fiction%20writers&ns%5B0%5D=1&templates_any=Infobox%20writer%0D%0AInfobox%20person&search_max_results=500&interface_language=en&)
* [Scientists](https://petscan.wmflabs.org/?language=en&project=wikipedia&depth=10&categories=Scientists&negcats=Fictional%20scientists&ns%5B0%5D=1&templates_any=Infobox%20person&search_max_results=500&interface_language=en&)