class DataPoint:
  def __init__(self, time, raw):
    self.time = time
    self.raw = int(raw)
    self.filtered = int(raw)

  def __str__(self):
    return "{} {}".format(self.time, self.raw)