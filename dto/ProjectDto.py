class ProjectDto:
  id: str | None 
  name: str
  color: str
  isArchived: bool
  
  def __init__(self, name: str, color: str, isArchived: bool = False):
    self.id = None  # This will be assigned during project creation
    self.name = name
    self.color = color
    self.isArchived = isArchived
  def __init__(self, name: str, color: str, isArchived: bool = False, id: str | None = None):
    self.id = id  # This will be assigned during project creation
    self.name = name
    self.color = color
    self.isArchived = isArchived
  
  def parseJson(raw: any, theId: str | None = None):
    name = raw.get('name')
    color = raw.get('color')
    isArchived = raw.get('isArchived')
    return ProjectDto(name, color, isArchived, theId)
