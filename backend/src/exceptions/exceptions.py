from fastapi import HTTPException

notAdminException = HTTPException(status_code=403, detail="Operation not permitted")

notFoundException = HTTPException(status_code=404, detail="Item not found")

fetchErrorException = HTTPException(status_code=500, detail="Error occurred while fetching data from the database")