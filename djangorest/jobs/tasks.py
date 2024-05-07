from celery import shared_task

@shared_task
def process_string(input_string):
    # Dummy function to simulate processing
    print(f"Processing the string: {input_string}")
    # Imagine this saves the result to a database
    # For now, it just returns the reversed string
    return input_string[::-1]
