"""Read documents: PDF to text, then split into chunks."""




class UnsupportedDocument(ValueError):
    """Raised when a file type we cannot read is uploaded."""
    