# Formula 1 Azure ETL Project

This project is part of my course attendance about Azure Databricks, using the Udemy platform. There is a certificate available at this link [Udemy Certificate](https://ude.my/UC-e54cd93d-2409-4334-8495-18a514c3c0d3) that serves as proof of completion. The aim of this project is to extract Formula 1 data from the Ergast API (via manual download), transform the data to make it suitable for presentation queries, and finally, load it into a storage container for future use.

![f1_project_graph](https://github.com/dmoralis/AirflowETLWeatherProject/assets/56253720/c62296be-61a8-4df1-8d62-cb3f92a40941)

*Image source: Azure Databricks & Spark For Data Engineers (PySpark / SQL) Course by Ramesh Retnasamy*

## Technologies Utilized

- **Azure Databricks**: The heart of our data transformation and analysis efforts.
- **PySpark - SQL**: The primary languages enabling data manipulation and querying.
- **Azure Workspace**: Our collaborative work environment.
- **Azure Resource Group**: For efficient resource management.
- **Azure Data Lake Gen2**: The repository of our data, providing scalability and reliability.
- **Azure Data Factory**: Orchestrating our ETL processes.
- **Azure Delta Lake**: Enhancing our data lake with transactional capabilities.
- **Unity Catalog**: Providing a centralized metadata repository.

## Data Insight

The tables in the Formula 1 dataset are as follows:

- **Circuits** (CSV)
- **Races** (CSV)
- **Constructors** (Single Line JSON)
- **Drivers** (Single Line Nested JSON)
- **Results** (Single Line JSON)
- **PitStops** (Multi Line JSON)
- **LapTimes** (Split CSV Files)
- **Qualifying** (Split Multi Line JSON Files)

Each of these tables comes with a clear name and serves a distinct purpose. For a deeper understanding of these tables, you can refer to the official user guide available here: F1DB User Guide.

## Project Details

### Storage
Our project uses Azure Data Lake Gen2 throughout its journey, divided into three phases: Bronze, Silver, and Gold, each in its own container:

- **Bronze**: Where we store the raw, untouched data.
- **Silver**: Data refinement takes place here, preparing it for deeper analysis.
- **Gold**: The data undergoes the most transformation and is ready for in-depth analysis.


### Ingestion & Transformation


**Azure Databricks** emerges as the tool behind data ingestion and transformation. We employ Notebooks, a dedicated Cluster, and leverage the PySpark and SQL languages to craft this transformation ([Formula1.zip](https://github.com/dmoralis/Azure-ETL-Formula1-Project/blob/64cdd010df42b361459a245a0f73c9099a1cd4ef/Formula1.zip)). The process unfolds as follows:

- Data is extracted from Formula 1 files that was manually uploaded to the Bronze container.
- Column names are converted from Camel Case to Snake Case, ensuring consistency.
- Processed data are stored by delta format in a defined schema, with the Silver container serving as its storage location.
- Production-level tables are crafted, residing in a schema with the Gold container as the base location. The crafted tables are delta formated too and include:
  - **race_results**
  - **driver_standings**
  - **constructor_standings**
  - **calculated_race_results**

Data is incrementally added to the Delta Lake Gen2 every week, categorized as both **Dimension** and **Fact** delta tables. Dimension tables undergo a **Full Load** due to their static nature, while Fact tables need an **Incremental Load** because of their size and frequent updates. The dimension tables comprise Circuits, Races, Constructors, and Drivers, while the fact tables consist of Results, PitStops, LapTimes, and Qualifying. In order to facilitate incremental loading, two additional columns, **create_date** and **update_date**, are appended to each Fact table to monitor data updates and support dynamic calculated tables.

The data update process varies as follows:
- Full Load data is overwritten every week.
- Incremental data utilizes the **Merge** command, exclusive to Delta tables (not Parquet), to replace and add new data based on matching primary keys between new and existing data.

### Configuration

To use the Storage Containers from Databricks Notebooks, a configuration method needs to be set up between the two services. The distinct options for this purpose are:

- **Access Key**: Create an access key from the Key Vault, safeguarded in Databricks Secrets for enhanced security. Access the containers using **abfss**.

- **Shared Access Signature (SAS)**: Ideal for short-term and low-permission access. Generate a SAS token for the container and incorporate it into Databricks Secrets. Configure your setup using these credentials.

- **Service Principal (Used in this project)**: Leverage a Service Principal with a client secret, enhancing security. Configure your setup using the **abfss** to access the desired container.

Additionally, **dbutils.fs.mount** command is employed to streamline container access through Service Principal credentials, simplifying data retrieval without relying on abfss links.

### Dashboards

After creating the Presentation tables, dashboards can be created from within the Databricks Notebook. In this example, the tables used are the calculated_race_results.

<img src="https://github.com/dmoralis/AzureETLFormula1Project/assets/56253720/d6750208-8265-4837-a401-88034622a325"  width="48%" height="250px">
<img src="https://github.com/dmoralis/AzureETLFormula1Project/assets/56253720/7aeceb32-1317-43e2-a55d-d6c5e761ba8d"  width="48%" height="250px">

### Pipeline Orchestration & Schedule

While pipeline orchestration can be managed within the Databricks Workflow section, we opt for a more robust solution, Azure Data Factory. Our pipeline comprises two distinct sub-pipelines: Ingestion and Transformation. To ensure error-free execution, we implement If-statements and schedule the pipelines to run on a **Tumbling Window** trigger. This trigger activates every week on Sundays, along with F1 race events, and it provides a dynamic **p_window_end_date** parameter at the close of the trigger window.


### Unity Catalog

Unity Catalog is examined in this project due to the capabilities offering:

- Data Discoverability: Easily search for data and find schema information
- Data Audit: Keep track of who accesses your data with user-level audit logs
- Data Lineage: Understand the journey of your data through the pipeline, including where it originated (upstream), how it has been modified, and where it's headed (downstream).
- Centralized Access Control: Manage data access policies across multiple workspaces using an inheritance model.

During this course, we created a demo project to utilize the Unity Catalog Metastore. We gained access to tables from both managed and external table scopes, all while exploring these powerful features through the user-friendly Databricks UI.


*Source file: [Formula1.zip](https://github.com/dmoralis/Azure-ETL-Formula1-Project/blob/64cdd010df42b361459a245a0f73c9099a1cd4ef/Formula1.zip)*
