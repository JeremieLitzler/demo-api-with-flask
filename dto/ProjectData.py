class ProjectData:
  def __init__(self, name: str, color: str, isArchived: bool = False):
    self.id = None  # This will be assigned during project creation
    self.name = name
    self.color = color
    self.isArchived = isArchived
  # def __init__(self, id: str, name: str, color: str, isArchived: bool = False):
  #   self.id = id  # This will be assigned during project creation
  #   self.name = name
  #   self.color = color
  #   self.isArchived = isArchived
