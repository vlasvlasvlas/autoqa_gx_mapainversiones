# GX
import great_expectations as gx
from great_expectations.checkpoint import Checkpoint
from great_expectations.data_context.types.resource_identifiers import (
    ValidationResultIdentifier,
)
from great_expectations.expectations.expectation import ExpectationConfiguration

# ENV
import os, sys
from dotenv import load_dotenv
from datetime import datetime, timezone

# Load environment variables
load_dotenv()


# Data Vars:
# db connection string
db = os.getenv("SQL_CONNSTRING_DB")
datasource_name = "sql_pan_stg"
my_checkpoint_name = "my_sql_checkpoint"

# Load the gx context
# The context serves as an entry point for GX operations and holds all relevant configurations.
context = gx.get_context()

connection_string = (
    os.getenv("SQL_CONNSTRING_PRE") + db + os.getenv("SQL_CONNSTRING_POST")
)

print(connection_string)

# doc:
# https://docs.greatexpectations.io/docs/oss/guides/connecting_to_your_data/fluent/database/connect_sql_source_data/

# create a SQL Data Source :
# add your dataset to this context as a Data Source to start interacting with the data.
# datasource_sql_pan_stg = context.sources.add_sql(
#     name="sql_pan_stg", connection_string=connection_string
# )

datasources = context.list_datasources()
datasource_names = [ds["name"] for ds in datasources]

if datasource_name not in datasource_names:

    print(f"Datasource {datasource_name} does not exist.")
    # create a SQL Data Source :
    # add your dataset to this context as a Data Source to start interacting with the data.
    datasource_sql_pan_stg = context.sources.add_sql(
        name=datasource_name, connection_string=connection_string
    )

    # data assets
    # Define Data Assets to specify the subset of data you'd like to work with. The asset can be as simple as full tables, or be as complex as a custom Data Analysis Expressions (DAX) query.

    # check tabla
    asset_name = "asset_1_pan_stg_ejecucion"
    asset_table_schema = "dbo"
    asset_table_name = "mef_vw_ejecucion"

    # add table asset
    table_asset = datasource_sql_pan_stg.add_table_asset(
        name=asset_name, schema_name=asset_table_schema, table_name=asset_table_name
    )

    # DAX
    # If you'd like to define your own measures or have more control over specific rows, you can add a DAX asset with a custom DAX query.

    # build batch request
    # https://docs.greatexpectations.io/docs/reference/learn/terms/batch_request/
    batch_request = datasource_sql_pan_stg.get_asset(
        asset_name
    ).build_batch_request()

    print(batch_request)

    # Expectation suite
    # In order to add specific constraints to the assets, you first have to configure Expectation Suites. After adding individual Expectations to each suite, you can then update the Data Context set up in the beginning with the new suite.

    # Great Expectations utiliza el concepto de "expectation suites", que son colecciones de expectativas que definen cómo deberían comportarse tus datos. Cada expectativa es una regla o prueba específica que tus datos deben cumplir.
    # Por ejemplo, una expectativa común es que los valores de una columna no deben ser nulos. Otra expectativa común es que los valores de una columna deben estar dentro de un rango específico.
    # Para crear una expectativa, primero debes crear una expectativa suite. Luego, puedes agregar expectativas a la suite.

    # suite name
    expectation_suite_name = "expectativas_pan_stg_ejecucion"

    suite_store = context.add_expectation_suite(expectation_suite_name)

    # add expectations:
    # https://greatexpectations.io/expectations

    # Mediante Expectation Configurations: Este método es más estructurado y te permite definir expectativas como configuraciones que luego se añaden a una suite de expectaciones. Esto es útil para cuando quieres mantener un código más modular y reusable, especialmente si las mismas expectativas se aplicarán a diferentes conjuntos de datos o en diferentes momentos.

    # 1. expect_column_values_to_not_be_null
    suite_store.add_expectation(
        ExpectationConfiguration(
            "expect_column_values_to_not_be_null", {"column": "anio"}
        )
    )

    context.add_or_update_expectation_suite(expectation_suite=suite_store)

    # Optional:
    # Run assert "my_expectation_suite" in context.list_expectation_suite_names() to veriify the Expectation Suite was created.

    # Crea expectativas directamente con el Validator: Este método permite añadir expectativas directamente al objeto validator y luego guardarlas como parte de la suite de expectaciones. Es útil para pruebas rápidas y experimentación porque puedes verificar las expectativas al vuelo.

    # Añade expectativas directamente usando el método de configuración del validator:
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=expectation_suite_name,
    )

    validator.expect_column_values_to_not_be_null(column="gasto")

    validator.head()

    # Run the following command to save your Expectation Suite
    validator.save_expectation_suite(discard_failed_expectations=False)

    context = context.convert_to_file_context()

    # Validate your data
    # You'll create and store a Checkpoint for your Batch, which you can use to validate and run post-validation actions.

    checkpoint = Checkpoint(
        name=my_checkpoint_name,
        run_name_template="%Y%m%d-%H%M%S-my-run-name-template",
        data_context=context,
        batch_request=batch_request,
        expectation_suite_name=expectation_suite_name,
        action_list=[
            {
                "name": "store_validation_result",
                "action": {"class_name": "StoreValidationResultAction"},
            },
            {
                "name": "update_data_docs",
                "action": {"class_name": "UpdateDataDocsAction"},
            },
        ],
    )

    # save checkpoint
    context.add_or_update_checkpoint(checkpoint=checkpoint)

else:
    print(f"Datasource {datasource_name} exists.")
    # verify the Expectation Suite was created:
    print("verify the Expectation Suite was created:")
    print(context.list_expectation_suite_names())
    checkpoint = context.get_checkpoint(my_checkpoint_name)


# run checkpoint
result = checkpoint.run()
context.open_data_docs()

print(result)
