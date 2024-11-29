import logging

def write_log(type, message):
  logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-18s %(name)-8s %(levelname)-8s %(message)s",
    datefmt="%y-%m-%d %H:%M",
  )
  if type == "info":
    logging.info(message)
  elif type == "warning":
    logging.warning(message)
  elif type == "error":
    logging.error(message)
  elif type == "critical":
    logging.critical(message)
  else:
    logging.debug(message)
