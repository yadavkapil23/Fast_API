from fastapi import FastAPI,Depends

@app.get("/profile")
def get_profile(user = Depends(verify_token)):
    return {"message": f"Hello {user['username']}"}

# Admin only endpoint
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    admin = Depends(require_admin),  # Must be admin
    db = Depends(get_db)
):
    # Delete user logic
    return {"message": f"User {user_id} deleted by admin"}