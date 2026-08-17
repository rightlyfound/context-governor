# Hidden Environment Variable Example

The service reads `SERVICE_PORT` directly from the environment without documenting or validating it. The expected fix is to document the variable and provide a safe default or clear startup error.
