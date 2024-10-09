# Main files in this folder

- `report.qmd`: The main Quarto document containing the full project report, including background, methodology, analysis, and results. 

To compile an up to date version of the report (stored as report.html and report.pdf), install Quarto, navigate to this folder, and run:

```
quarto render report.qmd
```

- `styles.css`: CSS file for styling the HTML output of the report. report.qmd draws on this file to style itself automatically.

- `16-irisqlin-kasra-mikalite-kb.pdf` is a pdf of the html version of report.qmd as it was rendered on 2024-10-07.

## Notes on Quarto

This project uses Quarto for report generation. Some of the reasons for this choice include:

1. **Multi-language support**: Quarto allows integration of Python, R, and markdown in a single document. This is important for our project, which uses both Python (for data processing) and R (for statistical analysis and visualization).

2. **Rich output options**: Quarto supports multiple output formats (HTML, PDF, Word) with a single source document. We primarily use HTML for its custom stylability and ease with which rendered html can be converted to a nice looking pdf. Future outputs of the project may include other formats; quarto makes it easy to swap between them.

3. **Customizable styling**: The accompanying `styles.css` file allows us to quickly and consistently adjust the appearance of the report without needing to manually adjust individual elements.
