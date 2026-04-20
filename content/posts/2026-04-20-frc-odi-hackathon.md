---
title: "FRC x ODI Open Structured Company Data Innovation Sprint"
date: "2026-04-20 17:09:48 +0100 BST"
tags: [hackathon, work]
---

At the end of March, Ellie, Madhav and I participated in the Financial Reporting Council and Open Data Institute Innovation Sprint. The event was aimed at active problem solvers to look at various aspects that relate to the economy – be it developers of data scientists, fintech or regtech innovators, analysts or investors, accountants and auditors, academics and researchers, policymakers, regulators, and end users as in companies. 

## Context
The hackathon was a full day event, but there was a preparatory session the day before, and it focused on the XBRL format, which is the standard for sharing financial or annotating financial data. 
For someone without much context to XBRL and financial reporting, this was an insightful session as it explained a lot of the concepts behind that format.

The annual reports that companies submit are annotated using XBRL, then submitted to the corresponding organizations. Private companies to the Companies House, charities to the Charity Commission, and public companies to the Financial Conduct Authority and Companies House. 

At a very high level, XBRL has things like concepts, entities, periods and units, as well as dimensions. 
* `Concept` – a piece of data is a concept– what is this data about? For example, revenue. 
* `Unit` – e.g. the currency, weight, percentage etc). 
* `Period` - a point in time (2026), or it could be duration (from April 2025 to March 2026). 
* `Entity` - to whom this data belongs. Usually the entity is the company. Entities have a unique identifier (URN) which may be the company ID, or the legal entity identifier (LEI) that's used for public companies. But it could be the charity registration number. 
* `Fact` – the value of the different elements.

And under the standard, there's a taxonomy. Each taxonomy has schemas, or a dictionary that explains the various concepts. And some of them are interrelatable, that is they can have relationships. The schemas describe the various aspects such as 
* data type, whether monetary, a string, shares
* period types - instant or duration, 
* but it could be more abstract concepts

And based on the standard and the various schemas, there are various levels of validation and tools to do so.
The Financial Reporting Council built a viewer for iXBRL (inline XBRL) – when companies create their reports, they transform that into XHTML and then from PDF or Microsoft doc or other formats. and then the outputs get annotated – either by the accounting software or a specialized company. 

The preparatory session was well worth attending as we got to see how FRC use company data using their [Company and Organisational Data Explorer](https://www.frc.org.uk/library/digital-reporting/company-and-organisational-data-explorer/) (CODEx) which uses iXBRL and other datasets, enabling them to perform better data analysis and slice it through various lenses and snapshots.

### Why having a standard is important.
First and foremost, this relates to data consistency. That is, there's a known way to annotate free text, such as annual reports in a way that can be understood by people, as well as machines. So different software packages, different companies can work with a common set of concepts, consistently. 

There are various repositories where you can get this data. For example,
* the [Financial Conduct Authority's National Storage mechanism](https://www.fca.org.uk/markets/primary-markets/regulatory-disclosures/national-storage-mechanism) (FCA NSM) – a portal that gives access to regulated announcements and disclosed documents.
* the [UK iXBRL viewer](https://ukixbrlviewer.org.uk/) – contains data from the Companies House and or the FCA registries. 
* the [XBRL Filing Index](https://filings.xbrl.org ) – contains data from public filings across multiple countries.


## The hackathon

On the day, there was a mix of developers, analysts, auditors, accountants, policy makers, open data advocates, as well as a few end-users (i.e. people that represent companies).

There were four main themes to explore at the hackathon.

1. Structured data for small and medium for SME finance and investment. So what changes if companies' house data is treated as a reusable trusted foundation for some finance and investment decisions. 
2. Trusting the tags –  that is, looking at measuring the quality of digital reporting. The focus was on the tagging quality, not what you know, the tagged information is. So it's looking at whether things are correctly tagged, they are correctly presented, as well as validated, and are all of the required tags there, and so on, and looking, can one create a confidence score. 
3. The third challenge was around AI optimizations and looking at whether XBRL is efficiently structured for AI or what kind of changes would be needed to make it easier for AI and LLMs to work with this data. 
4. Last but not least, the fourth challenge was policy intelligence at scale. So using structured company data for policy design, research and response. And this is exploring how structured company data is if treated as core economic infrastructure can be combined with other public data sets to support better policy decisions, be it kind of. 

### Resources 
The FRC and ODI teams put together a really good set of resources that could be used for the challenges. They ranged from  the Companies House bulk company data / bulk accounts data, to instructions to get access to the Companies House API to get information on company profiles, filing history and so on, to the [UK iXBRL viewer](https://ukixbrlviewer.org.uk/), a helpful Streamlit app to [convert XBRL to CSV](https://xbrl-to-csv.streamlit.app/). There was the [DBT “stream read XBRL”](https://stream-read-xbrl.docs.trade.gov.uk/) package to convert zipped Companies House data into data frames, and more. 

Additionally, the team compiled specific datasets and tools for each challenge, be it public data sets such as the ONS Geographic Area Economic Data, DSIT innovation clusters map, gender pay gap data, and more. Or things like the tools like Fandascope to check for tag inconsistency and presentation diagnostics or the US filing data checks, as well as the ML Commons croissant, (the machine learning ready dataset metadata format). 

### Process
Once the initial coffee and introductions were done, we chose a theme, split up in groups for each theme, got further context, then brainstormed ideas and debated the various approaches to narrow down what we focussed on. And then also set up to set out to try to build some tooling and also explore what is possible. As with any hackathon, there was a bit of initial chaos, but we had facilitators and advisors from FRC to help steer and advise us on different aspects of XBRL format.

Our team had quite a wide array of ideas, ranging from looking at custom tagging and identifying whether there are patterns within different industries that could be useful to fold back into the FRC taxonomies, as well as a benchmarking app, looking at tag gaps and suggesting different tags based on peer/industry usage. We also looked at the proximity of different tags, as well as and explored whether the regulation around tagging around using XBRL is accessible enough and how that might be made, whether that could be made more accessible and what those steps are. We had a look under the hood of the legal complexities involved in financial filings with XBRL documents in the UK which vary depending on whether the company is publicly listed or not, as well as the distinctions between the UKSEF (UK Single Electronic Format) used for filings with the FCA, which is meant to be a compliant alternative to ESEF (Europe Single Electronic Format).

The day ended with presentations from the various teams. I believe we had 8 or 9 different presentations and demos, ranging from data analysis, to LLM conversations, to prototypes. It was great to hear folks share some of the challenges they encountered, as well as future future steps.

Personally, I think it was a good event &mdash; we came out with a much better understanding of the financial reporting space, the standards, tooling and datasets available. More importantly, we took home a number of ideas and learnings, and are looking forward to seeing what comes off the back of the event, and hope that other organizations get inspired to run similar events.
