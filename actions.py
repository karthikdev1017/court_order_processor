import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ACTION_NAMES = {
    "issue_notice",
    "freeze_account",
    "release_funds",
    "suspend_accounts"
}

def issue_notice(customer_id):
    logger.info(f"Issuing notice for customer {customer_id}")
    return f"Issue notice for {customer_id}"

def freeze_account(customer_id):
    logger.info(f"Freezing account for customer {customer_id}")
    return f"Freeze account for {customer_id}"

def release_funds(customer_id):
    logger.info(f"Releasing funds for customer {customer_id}")
    return f"Release funds for {customer_id}"

def suspend_accounts(customer_id):
    logger.info(f"Suspending accounts for customer {customer_id}")
    return f"Suspend accounts for {customer_id}"

def execute_action(customer_id, action):
    try:
        if action not in ACTION_NAMES:
            logger.warning(f"Invalid action: {action}")
            return f"Invalid action '{action}'. Cannot process."
        action_func = globals()[action]
        result = action_func(customer_id)
        logger.info(f"Action {action} executed for customer {customer_id}: {result}")
        return result
    except Exception as e:
        logger.error(f"Error executing action {action}: {str(e)}")
        return f"Error executing action: {str(e)}"