from __future__ import annotations

from typing import Any

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import (
    BranchPythonOperator,
    PythonOperator,
)
from airflow.utils.trigger_rule import TriggerRule


DAG_ID = "doughflow_pizza_delivery"
TIMEZONE = "Asia/Kolkata"


SCHEDULE = "30 11,18 * * *"

# Default order 
DEFAULT_ORDER = {
    "order_id": "DF-20260821-001",
    "pizza": "Smoky Tandoori Crunch",
    "size": "Large",
    "delivery_zone": "Bhopal-West",
    "finish_type": "standard",
}



# TASK 1 - ORDER GATEWAY

def receive_order(**context: Any) -> dict[str, Any]:
    
    logger = context["ti"].log
    dag_run = context["dag_run"]

    
    api_conf = dag_run.conf or {}

    order = {
        "order_id": api_conf.get(
            "order_id",
            DEFAULT_ORDER["order_id"],
        ),
        "pizza": api_conf.get(
            "pizza",
            DEFAULT_ORDER["pizza"],
        ),
        "size": api_conf.get(
            "size",
            DEFAULT_ORDER["size"],
        ),
        "delivery_zone": api_conf.get(
            "delivery_zone",
            DEFAULT_ORDER["delivery_zone"],
        ),
        "finish_type": api_conf.get(
            "finish_type",
            DEFAULT_ORDER["finish_type"],
        ),
    }

    logger.info(
        "ORDER GATEWAY: Order %s has entered the kitchen.",
        order["order_id"],
    )

    logger.info(
        "ORDER GATEWAY: Pizza='%s', Size='%s', Zone='%s'.",
        order["pizza"],
        order["size"],
        order["delivery_zone"],
    )

    logger.info(
        "ORDER GATEWAY: Requested finish='%s'.",
        order["finish_type"],
    )

    logger.debug(
        "ORDER GATEWAY: Complete order packet=%s.",
        order,
    )

    logger.info(
        "ORDER GATEWAY: Order packet published to XCom.",
    )

    return order



# TASK 2 - DEMAND ROUTER


def classify_demand(**context: Any) -> dict[str, Any]:
   

    logger = context["ti"].log

    order = context["ti"].xcom_pull(
        task_ids="order_gateway",
    )

    if not order:
        logger.critical(
            "DEMAND ROUTER: No order packet received from XCom."
        )
        raise ValueError("Order packet missing from XCom.")

    logical_date = context["logical_date"]

    if logical_date.hour in {11, 12, 13, 18, 19, 20}:
        demand_level = "PEAK"
        priority = "EXPEDITED"
    else:
        demand_level = "NORMAL"
        priority = "STANDARD"

    order["demand_level"] = demand_level
    order["priority"] = priority

    logger.info(
        "DEMAND ROUTER: Order %s classified as %s demand.",
        order["order_id"],
        demand_level,
    )

    logger.info(
        "DEMAND ROUTER: Fulfillment priority=%s.",
        priority,
    )

    logger.debug(
        "DEMAND ROUTER: Updated order packet=%s.",
        order,
    )

    return order



# TASK 3 - DOUGH STATION


def prepare_dough(**context: Any) -> dict[str, Any]:
    

    logger = context["ti"].log

    order = context["ti"].xcom_pull(
        task_ids="demand_router",
    )

    if not order:
        logger.critical(
            "DOUGH STATION: Demand Router produced no order packet."
        )
        raise ValueError("Demand packet missing from XCom.")

    if order["demand_level"] == "PEAK":
        dough_profile = "FAST_RISE"
        preparation_minutes = 6
    else:
        dough_profile = "CLASSIC_RISE"
        preparation_minutes = 9

    order["dough_profile"] = dough_profile
    order["dough_minutes"] = preparation_minutes

    logger.info(
        "DOUGH STATION: Preparing order %s using %s profile.",
        order["order_id"],
        dough_profile,
    )

    logger.info(
        "DOUGH STATION: Estimated preparation time=%s minutes.",
        preparation_minutes,
    )

    logger.debug(
        "DOUGH STATION: Dough-ready packet=%s.",
        order,
    )

    return order



# TASK 4 - TOPPING ROUTE


def choose_finish_route(**context: Any) -> str:
   

    logger = context["ti"].log

    order = context["ti"].xcom_pull(
        task_ids="dough_station",
    )

    if not order:
        logger.critical(
            "TOPPING ROUTE: Dough Station produced no order packet."
        )
        raise ValueError("Dough packet missing from XCom.")

    finish_type = order.get(
        "finish_type",
        "standard",
    ).lower()

    logger.info(
        "TOPPING ROUTE: Order %s requested '%s' finishing.",
        order["order_id"],
        finish_type,
    )

    if finish_type == "premium":

        logger.info(
            "TOPPING ROUTE: Premium finishing route selected."
        )

        logger.warning(
            "TOPPING ROUTE: standard_finish will be SKIPPED "
            "because premium finishing was requested."
        )

        return "premium_finish"

    logger.info(
        "TOPPING ROUTE: Standard finishing route selected."
    )

    logger.warning(
        "TOPPING ROUTE: premium_finish will be SKIPPED "
        "because standard finishing was requested."
    )

    return "standard_finish"



# TASK 5A - PREMIUM FINISH


def apply_premium_finish(**context: Any) -> dict[str, Any]:
   

    logger = context["ti"].log

    order = context["ti"].xcom_pull(
        task_ids="dough_station",
    )

    if not order:
        logger.critical(
            "PREMIUM FINISH: No order packet received."
        )
        raise ValueError("Order packet missing.")

    order["finish_applied"] = "premium"
    order["finish_status"] = "COMPLETED"

    logger.info(
        "PREMIUM FINISH: Starting premium preparation for order %s.",
        order["order_id"],
    )

    logger.info(
        "PREMIUM FINISH: Premium toppings and finishing applied."
    )

    logger.info(
        "PREMIUM FINISH: Order %s is ready for oven processing.",
        order["order_id"],
    )

    logger.debug(
        "PREMIUM FINISH: Updated order packet=%s.",
        order,
    )

    return order



# TASK 5B - STANDARD FINISH


def apply_standard_finish(**context: Any) -> dict[str, Any]:
    

    logger = context["ti"].log

    order = context["ti"].xcom_pull(
        task_ids="dough_station",
    )

    if not order:
        logger.critical(
            "STANDARD FINISH: No order packet received."
        )
        raise ValueError("Order packet missing.")

    order["finish_applied"] = "standard"
    order["finish_status"] = "COMPLETED"

    logger.info(
        "STANDARD FINISH: Starting house finishing for order %s.",
        order["order_id"],
    )

    logger.info(
        "STANDARD FINISH: Standard toppings and seasoning applied."
    )

    logger.info(
        "STANDARD FINISH: Order %s is ready for oven processing.",
        order["order_id"],
    )

    logger.debug(
        "STANDARD FINISH: Updated order packet=%s.",
        order,
    )

    return order



# TASK 6 - OVEN WATCH


def monitor_oven(**context: Any) -> dict[str, Any]:
    
    logger = context["ti"].log
    task_instance = context["ti"]

    premium_order = task_instance.xcom_pull(
        task_ids="premium_finish",
    )

    standard_order = task_instance.xcom_pull(
        task_ids="standard_finish",
    )

    order = premium_order or standard_order

    if not order:
        logger.critical(
            "OVEN WATCH: Neither finishing station produced an order."
        )
        raise ValueError("Finished order packet missing.")

    if order["demand_level"] == "PEAK":
        bake_profile = "HIGH_THROUGHPUT"
        bake_minutes = 11
    else:
        bake_profile = "STANDARD_BAKE"
        bake_minutes = 13

    
    oven_temperature = 82

    minimum_temperature = 70
    maximum_temperature = 85

    logger.info(
        "OVEN WATCH: Starting bake for order %s.",
        order["order_id"],
    )

    logger.info(
        "OVEN WATCH: Selected profile=%s.",
        bake_profile,
    )

    logger.info(
        "OVEN WATCH: Estimated bake duration=%s minutes.",
        bake_minutes,
    )

    logger.info(
        "OVEN WATCH: Measured final temperature=%s°C.",
        oven_temperature,
    )

    if not (
        minimum_temperature
        <= oven_temperature
        <= maximum_temperature
    ):
        logger.critical(
            "OVEN WATCH: Order %s failed temperature validation.",
            order["order_id"],
        )
        raise ValueError(
            "Pizza failed oven temperature validation."
        )

    order["bake_profile"] = bake_profile
    order["bake_minutes"] = bake_minutes
    order["oven_temperature"] = oven_temperature
    order["quality_status"] = "PASS"

    logger.info(
        "OVEN WATCH: Quality validation PASSED for order %s.",
        order["order_id"],
    )

    logger.debug(
        "OVEN WATCH: Final baked order packet=%s.",
        order,
    )

    return order



# TASK 8 - COURIER HANDOFF

with DAG(
    dag_id=DAG_ID,
    description=(
        "DoughFlow automated pizza fulfillment pipeline "
        "for lunch and dinner rushes."
    ),
    start_date=pendulum.datetime(
        2026,
        8,
        1,
        tz=TIMEZONE,
    ),
    schedule=SCHEDULE,
    catchup=False,
    max_active_runs=1,
    tags=[
        "pizza",
        "doughflow",
        "automation",
        "assignment",
    ],
) as dag:

    order_gateway = PythonOperator(
        task_id="order_gateway",
        python_callable=receive_order,
    )

    demand_router = PythonOperator(
        task_id="demand_router",
        python_callable=classify_demand,
    )

    dough_station = PythonOperator(
        task_id="dough_station",
        python_callable=prepare_dough,
    )

    topping_route = BranchPythonOperator(
        task_id="topping_route",
        python_callable=choose_finish_route,
    )

    premium_finish = PythonOperator(
        task_id="premium_finish",
        python_callable=apply_premium_finish,
    )

    standard_finish = PythonOperator(
        task_id="standard_finish",
        python_callable=apply_standard_finish,
    )

    oven_watch = PythonOperator(
        task_id="oven_watch",
        python_callable=monitor_oven,
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    courier_handoff = BashOperator(
        task_id="courier_handoff",
        bash_command="""
            set -e

            echo "COURIER HANDOFF: Delivery system activated."
            echo "COURIER HANDOFF: Order ID = ${ORDER_ID}"
            echo "COURIER HANDOFF: Pizza = ${PIZZA}"
            echo "COURIER HANDOFF: Delivery Zone = ${DELIVERY_ZONE}"
            echo "COURIER HANDOFF: Finish = ${FINISH}"
            echo "COURIER HANDOFF: Quality = ${QUALITY}"
            echo "COURIER HANDOFF: Driver assignment confirmed."
            echo "COURIER HANDOFF: Order is OUT FOR DELIVERY."
        """,
        env={
            "ORDER_ID": (
                "{{ ti.xcom_pull(task_ids='oven_watch')"
                "['order_id'] }}"
            ),
            "PIZZA": (
                "{{ ti.xcom_pull(task_ids='oven_watch')"
                "['pizza'] }}"
            ),
            "DELIVERY_ZONE": (
                "{{ ti.xcom_pull(task_ids='oven_watch')"
                "['delivery_zone'] }}"
            ),
            "FINISH": (
                "{{ ti.xcom_pull(task_ids='oven_watch')"
                "['finish_applied'] }}"
            ),
            "QUALITY": (
                "{{ ti.xcom_pull(task_ids='oven_watch')"
                "['quality_status'] }}"
            ),
        },
        append_env=False,
    )

    
    # PIPELINE DEPENDENCIES
    

    order_gateway >> demand_router >> dough_station >> topping_route

    topping_route >> premium_finish
    topping_route >> standard_finish

    premium_finish >> oven_watch
    standard_finish >> oven_watch

    oven_watch >> courier_handoff
