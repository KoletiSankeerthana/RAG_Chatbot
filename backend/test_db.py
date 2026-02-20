try:
    from database import engine, Base
    import models # Ensure models are imported for Base.metadata.create_all
    
    # Create the database file and tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    print("Database connected successfully")
    print("SQLite database file 'chatbot.db' ensured and tables created.")
except Exception as e:
    print(f"Error connecting to database: {e}")
