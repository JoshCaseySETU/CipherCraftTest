import json
import os

def fetch_content(module_num, topic_num, page_num):
    try:
        print(f"Fetching content for: Module {module_num}, Topic {topic_num}, Page {page_num}")
        # Define the path to the JSON files folder
        folder_path = "CourseContent"
        print(f"Folder path: {folder_path}")
        
        # Load the JSON file corresponding to the module number
        file_path = os.path.join(folder_path, f"Module{module_num}.json")
        print(f"File path: {file_path}")
        with open(file_path, "r") as file:
            data = json.load(file)
                    
        # Adjust the index to be within the valid range
        module_num = min(max(module_num, 1), len(data["modules"]) - 1)

        # Retrieve the content based on the adjusted module number
        module = data["modules"][module_num - 1]

        topic = module["topics"][topic_num - 1]   
        
        title = topic.get('title', 'Default Title')
        narrative = topic.get('narrative', 'Default Narrative')
        
        page = topic["pages"][page_num - 1]  # Adjust index to 0-based
        
        
        interactive_component = False
        function_name = None
        if 'interactive' in page and page['interactive']:
            interactive_component = True
            function_name = page.get('function_name', '')
            interactive_component = page.get('interactive_component')
        if interactive_component:
            title = interactive_component.get('title', 'Default Title')
            input_fields = interactive_component.get('input_fields', [])

            # Now you can access individual input fields within the input_fields array
            for input_field in input_fields:
                label = input_field.get('label')
                input_type = input_field.get('type')
                field_id = input_field.get('id')

        # Return the content, interactive flag, and function name
        content = {
            'title': title,
            'narrative': narrative,
            'content': page.get('content', 'Default Content'),
            'image': page.get('image'),
            'interactive_component': interactive_component,
            'function_name': function_name,
            'video_url': page.get('video_url')
        }

        print("Content retrieved successfully.")
        return content
        
    except FileNotFoundError:
        error_msg = "Module not found."
        print(f"Error: {error_msg}")
        return {"error": error_msg}
    except IndexError:
        error_msg = "Topic or page not found."
        print(f"Error: {error_msg}")
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        print(f"Error: {error_msg}")
        return {"error": error_msg}


result= fetch_content(2,1,1)
print(result)
#result = fetch_content(2,1,1)
#print(result)
#result = fetch_content(3,1,1)
#print(result)
#result = fetch_content(4,1,1)
#print(result)
#result = fetch_content(5,1,1)
#print(result)

def next_page_func(module_num, topic_num, page_num):
    # Load the JSON file corresponding to the module number
    file_path = os.path.join("CourseContent", f"Module{module_num}.json")
    with open(file_path, "r") as file:
        data = json.load(file)

    # Retrieve the number of topics and pages in the current module and topic
    num_topics = len(data["modules"][module_num - 1]["topics"])
    num_pages = len(data["modules"][module_num - 1]["topics"][topic_num - 1]["pages"])

    # Check if there are more pages in the current topic
    if page_num < num_pages:
        return module_num, topic_num, page_num + 1
    else:
        # Check if there are more topics in the current module
        if topic_num < num_topics:
            return module_num, topic_num + 1, 1  # Move to the next topic
        else:
            # Check if there are more modules
            if module_num < len(data["modules"]):
                return module_num + 1, 1, 1  # Move to the next module
            else:
                # Reached the end of the content, reset to the first page of the first topic of the first module
                return 1, 1, 1

def prev_page_func(module_num, topic_num, page_num):
    # Load the JSON file corresponding to the module number
    file_path = os.path.join("CourseContent", f"Module{module_num}.json")
    with open(file_path, "r") as file:
        data = json.load(file)

    # Retrieve the number of topics and pages in the current module and topic
    num_topics = len(data["modules"][module_num - 1]["topics"])
    num_pages = len(data["modules"][module_num - 1]["topics"][topic_num - 1]["pages"])

    # Check if it's the first page
    if page_num == 1:
        # Check if it's the first topic
        if topic_num == 1:
            # Check if it's the first module
            if module_num == 1:
                # Already at the first page of the first topic of the first module
                # Wrap around to the last page of the last topic of the last module
                last_module = len(data["modules"])
                last_topic = len(data["modules"][last_module - 1]["topics"])
                last_page = len(data["modules"][last_module - 1]["topics"][last_topic - 1]["pages"])
                return last_module, last_topic, last_page
            else:
                # Move to the last page of the previous module
                prev_module = module_num - 1
                last_page = len(data["modules"][prev_module - 1]["topics"][-1]["pages"])
                return prev_module, num_topics, last_page
        else:
            # Move to the last page of the previous topic
            prev_topic = topic_num - 1
            last_page = len(data["modules"][module_num - 1]["topics"][prev_topic - 1]["pages"])
            return module_num, prev_topic, last_page
    else:
        # Move to the previous page
        return module_num, topic_num, page_num - 1


def is_module_completed(module_num, topic_num, page_num):
    try:
        # Load the JSON file corresponding to the module number
        file_path = os.path.join("CourseContent", f"Module{module_num}.json")
        with open(file_path, "r") as file:
            data = json.load(file)

        # Retrieve the number of topics in the current module
        num_topics = len(data["modules"])

        # Check if the specified module number is within the valid range
        if module_num < 1 or module_num > num_topics:
            return False

        # Retrieve the number of topics in the specified module
        num_topics = len(data["modules"][module_num - 1]["topics"])

        # Check if the specified topic number is within the valid range
        if topic_num < 1 or topic_num > num_topics:
            return False

        # Retrieve the number of pages in the specified topic
        num_pages = len(data["modules"][module_num - 1]["topics"][topic_num - 1]["pages"])

        # Check if the specified page number is within the valid range
        if page_num < 1 or page_num > num_pages:
            return False

        # Check if it's the last page of the last topic in the module
        return module_num == len(data["modules"]) and topic_num == num_topics and page_num == num_pages

    except FileNotFoundError:
        print("Error: Module not found.")
        return False
    except Exception as e:
        print(f"Error: An error occurred: {e}")
        return False


def fetch_pages_topic(module_num, topic_num):
    try:
        # Define the path to the JSON files folder
        folder_path = "CourseContent"
        
        # Load the JSON file corresponding to the module number
        file_path = os.path.join(folder_path, f"Module{module_num}.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        
        # Retrieve the topics for the specified module
        module = data["modules"][module_num]  # Adjust index to 0-based
        topic = module["topics"][topic_num - 1]  # Adjust index to 0-based
        
        # Calculate and return the total number of pages for the topic
        total_pages = len(topic["pages"])
        return total_pages
        
    except FileNotFoundError:
        print("Error: Module not found.")
        return 0
    except IndexError:
        print("Error: Topic not found.")
        return 0
    except Exception as e:
        print(f"Error: An error occurred: {e}")
        return 0

def fetch_content_backup(module_num, topic_num, page_num):
    try:
        print(f"Fetching content for: Module {module_num}, Topic {topic_num}, Page {page_num}")
        # Define the path to the JSON files folder
        folder_path = "CourseContent"
        print(f"Folder path: {folder_path}")
        

        file_path = os.path.join(folder_path, f"Module{module_num}.json")
        print(f"File path: {file_path}")
        with open(file_path, "r") as file:
            data = json.load(file)
        

        module = next((m for m in data["modules"] if m["id"] == str(module_num)), None)
        if module is None:
            raise ValueError(f"Module with id {module_num} not found")


        topic = next((t for t in module["topics"] if t["id"] == str(topic_num)), None)
        if topic is None:
            raise ValueError(f"Topic with id {topic_num} not found")


        page = next((p for p in topic["pages"] if p["id"] == str(page_num)), None)
        if page is None:
            raise ValueError(f"Page with id {page_num} not found")
        
        content = {
            'title': topic['title'],
            'narrative': topic['narrative'],
            'content': page['content']
        }
        print("Content retrieved successfully.")
        return content
        
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return {"error": f"File {file_path} not found."}
    except ValueError as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

def fetch_module_content(module_num):
    try:
        # Define the path to the JSON files folder
        folder_path = "CourseContent"
        
        # Load the JSON file corresponding to the module number
        file_path = os.path.join(folder_path, f"Module{module_num}.json")
        with open(file_path, "r") as file:
            data = json.load(file)
        
        # Extract content information from all topics and pages
        content_info = {}
        for module in data['modules']:
            for topic in module['topics']:
                for page in topic['pages']:
                    content_info.setdefault(topic['title'], []).append(page['content'])
                    
        print("ContentINFO = ", content_info)
        return content_info
    except FileNotFoundError:
        print("Error: Module not found.")
        return None
    except Exception as e:
        print(f"Error: An error occurred: {e}")
        return None


def update_page_content(module_num, topic_id, page_id, new_content):
    try:
        # Fetch the existing content
        module_content = fetch_module_content(module_num)
        if not module_content:
            return False
        
        # Find the module, topic, and page by their IDs
        module_found = False
        for module in module_content["modules"]:
            if module["id"] == module_num:
                for topic in module["topics"]:
                    if topic["id"] == topic_id:
                        for page in topic["pages"]:
                            if page["id"] == page_id:
                                page["content"] = new_content
                                module_found = True
                                break
                        break
                break
        
        if not module_found:
            print("Error: Module, topic, or page not found.")
            return False
        
        # Update the JSON file with the modified content
        folder_path = "CourseContent"
        file_path = os.path.join(folder_path, f"Module{module_num}.json")
        with open(file_path, "w") as file:
            json.dump(module_content, file, indent=4)
        
        return True
    except Exception as e:
        print(f"Error: An error occurred: {e}")
        return False


