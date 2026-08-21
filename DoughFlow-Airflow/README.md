# Operation: Slice of Success

## DoughFlow Pizza Delivery Pipeline

DoughFlow is an automated Apache Airflow pipeline designed to simulate
a pizza order moving from order reception to delivery.

## Pipeline Flow

The pipeline contains eight tasks:

1. Order Gateway
2. Demand Router
3. Dough Station
4. Topping Route
5. Premium Finish
6. Standard Finish
7. Oven Watch
8. Courier Handoff

The Order Gateway receives an order and stores the complete order packet
in XCom. The Demand Router retrieves the packet and classifies the
current kitchen demand as either PEAK or NORMAL. Dough Station then
selects an appropriate preparation profile.

Topping Route uses a BranchPythonOperator to decide whether the order
requires premium or standard finishing. The branch that is not selected
is deliberately skipped.

After finishing, Oven Watch receives the order from the selected branch,
performs a simulated baking and temperature validation, and marks the
order as ready. Finally, Courier Handoff uses a BashOperator to simulate
the delivery dispatch process.

## XCom

The order packet is passed between tasks using Airflow XCom.

Important values include:

- order_id
- pizza
- size
- delivery_zone
- finish_type
- demand_level
- priority

The order is initially created by Order Gateway and then enriched by
subsequent tasks.

## Branching and Skip Logic

The Topping Route task checks the `finish_type` supplied in the order.

If:

    finish_type = premium

the order is routed to `premium_finish`, while
`standard_finish` is deliberately skipped.

If:

    finish_type = standard

the order is routed to `standard_finish`, while
`premium_finish` is skipped.

This demonstrates Airflow branching and controlled task skipping.

## Schedule

The DAG runs at:

    11:30 AM
    6:30 PM

using the cron expression:

    30 11,18 * * *

These times represent the expected lunch and dinner pizza rushes.

## API Trigger

The final demonstration run is triggered through the Airflow REST API
using Swagger rather than the Airflow UI Trigger button.

The API request uses:

    POST /api/v1/dags/{dag_id}/dagRuns

The Swagger request supplies the order information through `dag_run.conf`,
including the requested finishing route.

## Logging

Every task produces meaningful Airflow task logs using Airflow's logger.
The logs record order identifiers, routing decisions, processing stages,
quality checks, and skip decisions.

No bare print statements are used in Python tasks.

## Final Demonstration

The Swagger-triggered premium order demonstrates:

    premium_finish  -> SUCCESS
    standard_finish -> SKIPPED

while the remaining pipeline completes successfully through
Courier Handoff.
