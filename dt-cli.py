import xmltodict

DT_PATH = "dt.xml"

def get_scene(scenes, scene_id):
    """Retrieve a scene by its ID."""
    for scene in scenes:
        if scene.get("@id") == scene_id:
            return scene
    return None  # Return None if the scene is not found

def get_choices(scene):
    """Display choices for a given scene and return the choices."""
    choices = scene.get("choices", {}).get("choice", [])

    # Handle single choice scenario
    if isinstance(choices, dict):
        print(f"Option (0): {choices.get('text')}")
        return [choices]
    
    # Handle multiple choices
    for i, choice in enumerate(choices):
        print(f"Option ({i}): {choice.get('text')}")
    
    return choices

def main():
    # Open and read the XML file
    with open(DT_PATH, 'r') as xml_file:
        xml_content = xml_file.read()

    # Convert XML to dictionary
    xml_dict = xmltodict.parse(xml_content)
    scenes = xml_dict.get("game", {}).get("scene", [])
    ending_scenes = xml_dict.get("game", {}).get("end", [])

    current_scene_id = 'start'
    ending_scene = None
    
    while ending_scene is None:
        current_scene = get_scene(scenes, current_scene_id)
        
        if current_scene is None:
            print("Current scene not found.")
            break

        print(current_scene.get("description"))
        choices = get_choices(current_scene)

        try:
            user_input = int(input("Enter an option: "))  # Convert input to an integer
            user_choice = choices[user_input]
            print(f"You chose to {user_choice.get('text')}.")

            next_scene_id = user_choice.get("@next")
            current_scene_id = next_scene_id
            ending_scene = get_scene(ending_scenes, next_scene_id)
        
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid option number.")

    if ending_scene:
        print(ending_scene.get("description"))

if __name__ == "__main__":
    main()
