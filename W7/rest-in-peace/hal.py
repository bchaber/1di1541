def add_link(document, rel, href):
  if "_links" not in document:
    document["_links"] = {}
  document["_links"][rel] = {"href": href}

def embed(document, name, resource):
  if "_embedded" not in document:
    document["_embedded"] = {}
  document["_embedded"][name] = resource
