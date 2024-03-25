import streamlit as st
import requests

# The base URL for your FastAPI backend
BASE_URL = "http://localhost:8000"

def get_heroes():
    """Fetches the list of heroes from the FastAPI backend."""
    response = requests.get(f"{BASE_URL}/heroes")
    return response.json()

def add_hero(hero):
    """Sends a request to add a new hero to the backend."""
    response = requests.post(f"{BASE_URL}/add_heroes", json=hero)
    return response.json()

def delete_hero(name):
    """Sends a request to delete a hero by name."""
    response = requests.delete(f"{BASE_URL}/delete_heroes/{name}")
    return response.json()

def update_hero(name):
    """Sends a request to update an existing hero."""
    response = requests.put(f"{BASE_URL}/update_heroes/{name}")
    return response.json()

def main():
    """Main function to render the Streamlit UI."""
    st.title("Hero Management System")

    # Displaying existing heroes
    st.subheader("Existing Heroes")
    heroes = get_heroes()
    for hero in heroes:
        st.write(f"Name: {hero['name']}, Secret Name: {hero['secret_name']}, Age: {hero.get('age', 'N/A')}, Location: {hero['location']}")

    # Adding a new hero
    st.subheader("Add a New Hero")
    with st.form("add_hero_form"):
        name = st.text_input("Name")
        secret_name = st.text_input("Secret Name")
        age = st.number_input("Age", min_value=0, value=30, step=1)
        location = st.text_input("Location")
        submitted = st.form_submit_button("Add Hero")
        if submitted:
            hero = {"name": name, "secret_name": secret_name, "age": age, "location": location}
            add_hero(hero)
            st.success("Hero added successfully!")

    # Deleting a hero
    st.subheader("Delete a Hero")
    delete_hero_name = st.text_input("Name of the hero to delete")
    if st.button("Delete Hero"):
        delete_hero(delete_hero_name)
        st.success("Hero deleted successfully!")
        
    # Updating a hero
    st.subheader("Update a Hero")
    with st.form("update_hero_form"):
        name = st.text_input("Name")
        secret_name = st.text_input("Secret Name")
        age = st.number_input("Age", min_value=0, value=30, step=1)
        location = st.text_input("Location")
        submitted = st.form_submit_button("Update Hero")
        if submitted:
            hero = {"name": name, "secret_name": secret_name, "age": age, "location": location}
            update_hero(hero)
            st.success("Hero updated successfully!")

if __name__ == "__main__":
    main()
