from functools import partial

def validate_required_properties(obj, required_properties):
  """
  This function checks if all required properties exist and are not empty (after trim for strings).

  Args:
      obj: The object to be validated.
      required_properties: A list of strings representing the required property names.

  Returns:
      None if all properties are valid, otherwise returns a dictionary containing an "error" key with a message.
  """
  missing_or_empty = []
  for prop in required_properties:
    value = getattr(obj, prop)
    if value is None or (isinstance(value, str) and value.strip() == ""):
      missing_or_empty.append(prop)
  if missing_or_empty:
    return {"error": f"Missing required properties: {', '.join(missing_or_empty)}"}
  return None